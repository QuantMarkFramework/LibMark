import unittest
import quantmark as qm

class TestVQEAlgorithm(unittest.TestCase):
	def setUp(self) -> None:
		self.optimizer = 'optimizer'
		self.backend = 'backend'
		self.molecule = 'molecule'
		self.circuit = 'circuit'
		self.hamiltonian = 'hamiltonian'

	def test_exception_when_no_molecule_and_no_hamiltonian_given(self):
		with self.assertRaises(Exception) as context:
			qm.VQEAlgorithm(
				optimizer=self.optimizer,
				backend=self.backend,
				circuit=self.circuit
			)
		self.assertTrue('You have give to a molecule or a hamiltonian.'
			in str(context.exception))

	def test_can_not_make_algorithm_with_molecule_and_hamiltonian(self):
		with self.assertRaises(Exception) as context:
			qm.VQEAlgorithm(
				optimizer=self.optimizer,
				backend=self.backend,
				hamiltonian=self.hamiltonian,
				molecule=self.molecule,
				circuit=self.circuit
			)
		self.assertTrue('You have give to a molecule or a hamiltonian not both.'
			in str(context.exception))

	def test_exception_when_trying_to_add_molecule_when_hamiltonian_exists(self):
		algorithm = qm.VQEAlgorithm(
			optimizer=self.optimizer,
			backend=self.backend,
			hamiltonian=self.hamiltonian,
			circuit=self.circuit
		)
		with self.assertRaises(Exception) as context:
			algorithm.molecule = 1
		self.assertTrue('Cannot set molecule when there is a hamiltonian.'
			in str(context.exception))

	def test_exception_when_trying_to_add_hamiltonian_when_molecule_exists(self):
		algorithm = qm.VQEAlgorithm(
			optimizer=self.optimizer,
			backend=self.backend,
			molecule=self.molecule,
			circuit=self.circuit
		)
		with self.assertRaises(Exception) as context:
			algorithm.hamiltonian = 1
		self.assertTrue('Cannot set hamiltonian when there is a molecule.'
			in str(context.exception))
