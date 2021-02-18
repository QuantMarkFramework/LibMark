import functools
import numpy as np


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
		return self._circuit.depth

	@property
	@functools.lru_cache()
	def qubit_count(self):
		return self._circuit.n_qubits

	def __str__(self):
		average = f'ACCURACY HISTORY:   {self.accuracy_history}\n' if self.accuracy_history else ''
		return (
			f'AVERAGE HISTORY:    {self.average_history}\n'
			f'{average}'
			f'QUBIT COUNT:        {self.qubit_count}\n'
			f'GATE DEPTH:         {self.gate_depth}\n'
			f'AVERAGE ITERATIONS: {self.average_iterations}\n'
			)
