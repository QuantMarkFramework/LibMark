from typing import List
from quantmark.qm_backend import QMBackend
from quantmark.qm_optimizer import QMOptimizer
import numpy as np
from tequila.circuit.circuit import QCircuit
from quantmark.circuit import CircuitInfo
from quantmark.decorators.cached import cached

CHEMICAL_ACCURACY = 1 / 627.5094740631


class VQEResult:
	"""
	The object returned when VQEAlgorithm is analyzed. Stores information about the algorithm and
	runs done during the analyzing process.

	Attributes
	----------
		average_history : List[float]
			The average values after minimizing iterations.
		accuracy_history : List[float]
			The average accuracy (compared to target_value) after minimizing iterations.
		value : float
			The average value after the last minimizing iteration.
		accuracy : float
			The difference in value compared to the target_value after the last minimizing
			iteration.
		success_rate : float
			The fraction of runs that got a result that is accurate to the FCI value with the
			accuracy '1 / 627.5094740631'.
		average_iterations : float
			The average amount of iterations that the minimizing process takes.
		max_iterations : int
			The highest amount of iterations the minimizing process took during analyzing.
		gate_depth : int
			The gate depth of the circuit.
		qubit_count : int
			The amount of qubits the circuit needs.
		gate_count : int
			The amount of gates the circuit uses.
		parameter_count : int
			The amount of parameters on the circuit that have to be optimized.
		results : list
			A list with the original results from the minimizing method.
		target_value : float
			The value that you hope the algorithm reaches. If this is None and the moleucule
			parameter is not none, the FCI method is used to calculate a target value for analysis.
		molecule :
			The target molecule.
		hamiltonian :
			The target hamiltonian.

	Methods
	----------
		__str__ : str
			Prints a list of some interesting attributes (one per line).
	"""
	def __init__(
		self,
		circuit: QCircuit,
		optimizer: QMOptimizer,
		backend: QMBackend,
		results: list,
		max_iterations: int,
		molecule=None,
		hamiltonian=None,
		target_value: float = None,
	):
		"""
		Creates a VQEResult object. This should not be used anywhere else than in the
		VQEAlgorithm.analyze method.

		Parameters
		----------
			circuit : QCircuit
				The quantum circuit that was used by the algorithm.
			optimizer : QMOptimizer
				The optimizer that was used by the algorithm.
			backend : QMBackend
				The backend that was used by the algorithm.
			results : list
				Information about the runs of the algorithm. (Contains results from the minimize
				method)
			max_iterations : int
				The maximum iterations for the minimizing process. After this the algorithm is
				forced to stop.
			molecule :
				The target molecule (can not coexist with a hamiltonian property).
			hamiltonian :
				The target hamiltonian (can not coexist with a molecule property).
			target_value:
				A custom target value that the algorithm should reach. If none given and a molecule
				is given, this is calulated with the FCI method.
		"""
		self._molecule = molecule
		self._circuit = circuit
		self._backend = backend
		self._results = results
		self._optimizer = optimizer
		self._hamiltonian = hamiltonian
		self._target_value = target_value
		self._circuit_info = CircuitInfo(circuit)
		self._user_set_max_iterations = max_iterations

	@property
	@cached
	def target_value(self):
		"""
		The value that you hope the algorithm reaches. If None and the moleucule parameter
		is not none, the FCI method is used to calculate a target value for analyzis.
		"""
		if self._target_value:
			return self.target_value
		if self._molecule:
			return self._molecule.compute_energy(method='fci')
		return None

	@property
	@cached
	def average_history(self) -> List[float]:
		"""The average values after minimizing iterations."""
		res = [i.history.energies.copy() for i in self._results]
		longest_history = max([len(i) for i in res])

		# Repeats last values to get a  matrix.
		for index, value in enumerate(res):
			target = value
			target_lenght = len(target)
			new_value = [target[target_lenght - 1]] * (longest_history - target_lenght)
			res[index] = target + new_value
		average_history = np.matrix(res).mean(0, dtype=np.float64).tolist()[0]
		return average_history

	@property
	def value(self) -> float:
		"""The average value after the last minimizing iteration."""
		return self.average_history[-1]

	@property
	@cached
	def max_iterations(self) -> int:
		"""The highest amount of iterations the minimizing process took during analyzing."""
		return len(self.average_history)

	@property
	@cached
	def average_iterations(self) -> float:
		"""The average amount of iterations that the minimizing process takes."""
		iteration_counts = [len(i.history.energies) for i in self._results]
		return sum(iteration_counts) / len(iteration_counts)

	@property
	@cached
	def accuracy_history(self) -> List[float]:
		"""The average accuracy (compared to target_value) after minimizing iterations."""
		if not self.target_value:
			return None
		return [abs(i - self.target_value) for i in self.average_history]

	@property
	def accuracy(self) -> float:
		"""
		The difference in value compared to the target_value after the last minimizing iteration.
		"""
		return self.accuracy_history[-1]

	@property
	def gate_depth(self) -> int:
		"""The gate depth of the circuit."""
		return self._circuit_info.gate_depth

	@property
	def qubit_count(self) -> int:
		"""The amount of qubits the circuit needs."""
		return self._circuit_info.qubit_count

	@property
	def gate_count(self) -> int:
		"""The amount of gates the circuit uses."""
		return self._circuit_info.gate_count

	@property
	def parameter_count(self) -> int:
		"""The amount of parameters on the circuit that have to be optimized."""
		return self._circuit_info.parameter_count

	@property
	@cached
	def success_rate(self) -> float:
		"""
		The fraction of runs that got a result that is accurate to the FCI value with the accuracy
		'1 / 627.5094740631'.
		"""
		if not self.target_value:
			return None
		success = 0
		for result in self._results:
			value = result.history.energies[-1]
			if abs(value - self.target_value) <= CHEMICAL_ACCURACY:
				success += 1
		return success / len(self._results)

	@property
	def results(self) -> list:
		"""A list with the original results from the minimizing method."""
		return self._results

	@property
	def molecule(self):
		"""The target molecule."""
		return self._molecule

	@property
	def hamiltonian(self):
		"""The target hamiltonian"""
		return self._hamiltonian

	def __str__(self):
		"""Prints a list of some interesting attributes (one per line)."""
		average = f'ACCURACY HISTORY:   {self.accuracy_history}\n' if self.accuracy_history else ''
		success_rate = ''
		if self.success_rate is not None:
			success_rate = f'SUCCESS RATE:       {self.success_rate}\n'
		warning = ""
		if self.max_iterations >= self._user_set_max_iterations:
			warning += "WARNING: Max iteration was reached!\n"
		return (
			f'{warning}'
			f'AVERAGE HISTORY:    {self.average_history}\n'
			f'{average}'
			f'QUBIT COUNT:        {self.qubit_count}\n'
			f'GATE DEPTH:         {self.gate_depth}\n'
			f'GATE COUNT:         {self.gate_count}\n'
			f'PARAMETER COUNT:    {self.parameter_count}\n'
			f'AVERAGE ITERATIONS: {self.average_iterations}\n'
			f'{success_rate}'
		)
