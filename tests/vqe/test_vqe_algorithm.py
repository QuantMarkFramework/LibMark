import unittest
from unittest.mock import MagicMock
import tequila as tq
import quantmark as qm

class TestVQEAlgorithm(unittest.TestCase):
	def setUp(self) -> None:
		self.optimizer = qm.QMOptimizer(module="scipy", method="BFGS")
		self.backend = qm.QMBackend(backend='qulacs')
		self.molecule = tq.Molecule(
			geometry='H 0. 0.0 0.0\nLi 0.0 0.0 1.6',
			basis_set='sto-3g',
			active_orbitals={'A1': [1], 'B1': [0] }
		)

		self.circuit = tq.gates.Ry(angle='a', target=0) + tq.gates.X(target=[2,3])
		self.circuit += tq.gates.X(control=0, target=1)
		self.circuit += tq.gates.X(target=2, control=0)
		self.circuit += tq.gates.X(target=3, control=1)

		self.algorithm = qm.VQEAlgorithm(
			optimizer=self.optimizer,
			backend=self.backend,
			molecule=self.molecule,
			circuit=self.circuit,
			repetitions=1
		)

	def test_analyze_runs_minimize(self):
		self.optimizer.minimize = MagicMock()

		self.algorithm.analyze()
		self.optimizer.minimize.assert_called_once()

	def test_result_gets_result_from_minimizer(self):
		self.optimizer.minimize = MagicMock(return_value='moi')

		result = self.algorithm.analyze()
		self.assertTrue(result.results[0], 'moi')

	def test_makes_hamiltonian(self):
		self.molecule.make_hamiltonian = MagicMock(
			return_value = self.molecule.make_hamiltonian()
		)
		self.algorithm.analyze()
		self.molecule.make_hamiltonian.assert_called_once()

	def test_exception_when_trying_to_add_hamiltonian_when_molecule_exists(self):
		with self.assertRaises(Exception) as context:
			self.algorithm.hamiltonian = 1
		self.assertTrue('Cannot set hamiltonian when there is a molecule.'
			in str(context.exception))
