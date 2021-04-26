import tequila as tq

from tequila.circuit import QCircuit as Circuit
from tequila import QubitHamiltonian
from quantmark.qm_backend import QMBackend as Backend
from quantmark.qm_optimizer import QMOptimizer as Optimizer
from quantmark.vqe.vqe_result import VQEResult as Result
from quantmark.circuit import CircuitInfo, circuit_from_string


class VQEAlgorithm:
	"""
	A class that holds all information about a Variational Quantum Algorithm. Used to analyze the
	algorithm.

	Attributes
	----------
		circuit : QCircuit
			The quantum circuit of the algorithm.
		optimizer : QMOptimizer
			The optimizer of the algorithm.
		molecule :
			The target molecule (can not coexist with a hamiltonian property).
		hamiltonian : QubitHamiltonian
			The target hamiltonian (can not coexist with a molecule property).
		backend : QMBackend
			The backend (simulator) that the algorithm uses for quantum computation.
		silent : bool
			If True the minimizing process will not print information while it is running.
		repetitions : int
			The amount of times the algorithm is run during analyzing to get average values.
		target_value : float
			The value that you hope the algorithm reaches. If None and the moleucule parameter
			is not none, the FCI method is used to calculate a target value for analyzis.

	Methods
	-------
		analyze_circuit() -> CircuitInfo:
			Analyzes only the circuit without running the algorithm.
		analyze(self) -> VQEResult:
			Analyzes the algorithm. This runs the algorithm many times (repetitions) meaning that it
			can take a long time.
	"""
	def __init__(
		self,
		circuit: Circuit,
		optimizer: Optimizer = Optimizer(),
		backend: Backend = Backend(),
		molecule=None,
		hamiltonian: QubitHamiltonian = None,
		silent: bool = True,
		repetitions: int = 10,
		target_value: float = None
	):
		"""
		Creates a VQEAlgorithm object.

		Parameters
		----------
			circuit : QCircuit
				The quantum circuit to be used.
			optimizer : QMOptimizer
				The optimizer to be used.
			backend : QMBackend
				The backend (simulator) to be used to run the quantum part of the algorithm.
			molecule :
				The molecule to be inspected (can not be given when hamiltonian is given).
			hamiltonian : QubitHamiltonian
				The hamiltonian to be inspected (can not be given when molecule is given).
			silent : bool
				If True the minimizing process will not print information while it is running.
			repetitions : int
				The amount of times the algorithm should run during analyzing to get average values.
			target_value : float
				The value that you hope the algorithm reaches. If None and the moleucule parameter
				is not none, the FCI method is used to calculate a target value for analyzis.
		"""
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
		"""The quantum circuit of the algorithm."""
		return self._circuit

	@circuit.setter
	def circuit(self, circuit):
		if isinstance(circuit, str):
			circuit = circuit_from_string(circuit)
		self._circuit = circuit

	@property
	def optimizer(self):
		"""The optimizer of the algorithm."""
		return self._optimizer

	@optimizer.setter
	def optimizer(self, optimizer):
		self._optimizer = optimizer

	@property
	def molecule(self):
		"""The target molecule (can not coexist with a hamiltonian property)."""
		return self._molecule

	@molecule.setter
	def molecule(self, molecule):
		if self._hamiltonian:
			raise Exception('Cannot set molecule when there is a hamiltonian.')
		self._molecule = molecule

	@property
	def hamiltonian(self):
		"""The target hamiltonian (can not coexist with a molecule property)."""
		return self._hamiltonian

	@hamiltonian.setter
	def hamiltonian(self, hamiltonian):
		if self._molecule:
			raise Exception('Cannot set hamiltonian when there is a molecule.')
		self._hamiltonian = hamiltonian

	@property
	def backend(self):
		"""The backend (simulator) that the algorithm uses for quantum computation."""
		return self._backend

	@backend.setter
	def backend(self, backend):
		self._backend = backend

	@property
	def silent(self):
		"""If True the minimizing process will not print information while it is running."""
		return self._silent

	@silent.setter
	def silent(self, silent):
		self._silent = silent

	@property
	def repetitions(self):
		"""The amount of times the algorithm is run during analyzing to get average values."""
		return self._repetitions

	@repetitions.setter
	def repetitions(self, repetitions):
		self._repetitions = repetitions

	@property
	def target_value(self):
		"""
		The value that you hope the algorithm reaches. If None and the moleucule parameter is not
		none, the FCi method is used to calculate a target value for analyzis.
		"""
		return self._target_value

	@target_value.setter
	def target_value(self, target_value):
		self._target_value = target_value

	def analyze_circuit(self) -> CircuitInfo:
		"""
		Analyzes only the circuit without running the algorithm.

		Returns
		----------
		A CircuitInfo object that stores information about the circuit.
		"""
		return CircuitInfo(self.circuit)

	def analyze(self) -> Result:
		"""
		Analyzes the algorithm. This runs the algorithm many times (repetitions) meaning that it
		can take a long time.

		Returns
		----------
		A VQEResult object that stores information about the algorithm and the runs of it. The VQEResult
		object can be used to get information about the algorithm.
		"""
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
		return Result(
			self._circuit,
			self._optimizer,
			self._backend,
			results,
			molecule=self._molecule,
			target_value=self._target_value
		)
