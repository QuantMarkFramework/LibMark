import tequila as tq

from tequila.circuit import QCircuit as Circuit
from tequila import QubitHamiltonian
from quantmark.qm_backend import QMBackend as Backend
from quantmark.qm_optimizer import QMOptimizer as Optimizer
from quantmark.vqe.vqe_result import VQEResult as Result
from quantmark.circuit import circuit_from_string

class VQEAlgorithm:
	def __init__(
		self,
		circuit: Circuit,
		optimizer: Optimizer = Optimizer(),
		backend: Backend = Backend(),
		molecule = None,
		hamiltonian: QubitHamiltonian = None,
		silent: bool = True,
		repetitions: int = 100,
		target_value: int = None
		):
		if not molecule and not hamiltonian:
			raise Exception('You have give to a molecule or a hamiltonian.')
		if molecule and hamiltonian:
			raise Exception('You have give to a molecule or a hamiltonian not both.')
		self._circuit = circuit
		self._optimizer = optimizer
		self._backend = backend
		self._molecule = molecule
		self._hamiltonian = hamiltonian
		self._silent = silent
		self._repetitions = repetitions
		self._target_value = target_value

	@property
	def circuit(self):
		return self._circuit

	@circuit.setter
	def circuit(self, circuit):
		if isinstance(circuit, str):
			circuit = circuit_from_string(circuit)
		self._circuit = circuit

	@property
	def optimizer(self):
		return self._optimizer

	@optimizer.setter
	def optimizer(self, optimizer):
		self._optimizer = optimizer

	@property
	def molecule(self):
		return self._molecule

	@molecule.setter
	def molecule(self, molecule):
		if self._hamiltonian:
			raise Exception('Cannot set molecule when there is a hamiltonian.')
		self._molecule = molecule

	@property
	def hamiltonian(self):
		return self._hamiltonian

	@hamiltonian.setter
	def hamiltonian(self, hamiltonian):
		if self._molecule:
			raise Exception('Cannot set hamiltonian when there is a molecule.')
		self._hamiltonian = hamiltonian

	@property
	def backend(self):
		return self._backend

	@backend.setter
	def backend(self, backend):
		self._backend = backend

	@property
	def silent(self):
		return self._silent

	@silent.setter
	def silent(self, silent):
		self._silent = silent

	@property
	def repetitions(self):
		return self._repetitions

	@repetitions.setter
	def repetitions(self, repetitions):
		self._repetitions = repetitions

	@property
	def target_value(self):
		return self._target_value

	@target_value.setter
	def target_value(self, target_value):
		self._target_value = target_value

	def analyze(self):
		if not self._molecule and not self._hamiltonian:
			raise Exception('You have give to a molecule or a hamiltonian.')
		if self._molecule and self._hamiltonian:
			raise Exception('You have give to a molecule or a hamiltonian not both.')
		if self._molecule:
			objective = tq.ExpectationValue(H=self._molecule.make_hamiltonian(), U=self._circuit)
		if self._hamiltonian:
			objective = tq.ExpectationValue(H=self._hamiltonian, U=self._circuit)

		results = [None] * self._repetitions
		for i in range(self._repetitions):
			results[i] = self._optimizer.minimize(
				objective=objective,
				backend=self._backend.backend,
				silent=self._silent)
		return Result(self._circuit,
			self._optimizer,
			self._backend,
			results,
			molecule=self._molecule,
			target_value=self._target_value)
