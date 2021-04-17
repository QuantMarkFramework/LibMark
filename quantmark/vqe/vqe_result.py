import functools
import numpy as np
from quantmark.circuit import CircuitInfo

CHEMICAL_ACCURACY = 1/627.5094740631

class VQEResult:
	"""
	Result from quantmark benchamrk.
	"""
	def __init__(self,
		circuit,
		optimizer,
		backend,
		results,
		molecule=None,
		hamiltonian=None,
		target_value=None
		):
		self._molecule = molecule
		self._circuit = circuit
		self._backend = backend
		self._results = results
		self._optimizer = optimizer
		self._hamiltonian = hamiltonian
		self._target_value = target_value
		self._circuit_info = CircuitInfo(circuit)

	@property
	@functools.lru_cache()
	def target_value(self):
		if self._target_value:
			return self.target_value
		if self._molecule:
			return self._molecule.compute_energy(method='fci')
		return None

	@property
	@functools.lru_cache()
	def average_history(self):
		res = [i.history.energies.copy() for i in self._results]
		longest_history = max([len(i) for i in res])

		# Repeats last values to get matrix
		for index, value in enumerate(res):
			target = value
			target_lenght = len(target)
			new_value = [target[target_lenght - 1]] * (longest_history-target_lenght)
			res[index] = target + new_value
		average_history=np.matrix(res).mean(0, dtype=np.float64).tolist()[0]
		return average_history

	@property
	@functools.lru_cache()
	def value(self):
		return self.average_history[-1]

	@property
	@functools.lru_cache()
	def max_iterations(self):
		return len(self.average_history)

	@property
	@functools.lru_cache()
	def average_iterations(self):
		iteration_counts = [len(i.history.energies) for i in self._results]
		return sum(iteration_counts)/len(iteration_counts)

	@property
	@functools.lru_cache()
	def accuracy_history(self):
		if not self.target_value:
			return None
		return [abs(i - self.target_value) for i in self.average_history]

	@property
	@functools.lru_cache()
	def accuracy(self):
		return self.accuracy_history[-1]

	@property
	@functools.lru_cache()
	def gate_depth(self):
		return self._circuit_info.gate_depth

	@property
	@functools.lru_cache()
	def qubit_count(self):
		return self._circuit_info.qubit_count

	@property
	@functools.lru_cache()
	def gate_count(self):
		return self._circuit_info.gate_count

	@property
	@functools.lru_cache()
	def parameter_count(self):
		return self._circuit_info.parameter_count

	@property
	@functools.lru_cache()
	def success_rate(self):
		if not self.target_value:
			return None
		success = 0
		for result in self._results:
			value = result.history.energies[-1]
			if abs(value - self.target_value) <= CHEMICAL_ACCURACY:
				success += 1
		return success / len(self._results)

	@property
	def results(self):
		return self._results

	def __str__(self):
		average = f'ACCURACY HISTORY:   {self.accuracy_history}\n' if self.accuracy_history else ''
		success_rate = ''
		if self.success_rate is not None:
			success_rate = f'SUCCESS RATE:       {self.success_rate}\n'
		return (
			f'AVERAGE HISTORY:    {self.average_history}\n'
			f'{average}'
			f'QUBIT COUNT:        {self.qubit_count}\n'
			f'GATE DEPTH:         {self.gate_depth}\n'
			f'GATE COUNT:         {self.gate_count}\n'
			f'PARAMETER COUNT:    {self.parameter_count}\n'
			f'AVERAGE ITERATIONS: {self.average_iterations}\n'
			f'{success_rate}'
			)
