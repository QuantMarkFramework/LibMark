import tequila as tq


class QMBackend():
	"""
	A class that holds information about a backend and can be given as a parameter to an algorithm.

	Attributes
	----------
		backend : str
			The name of the used backend (simulator).
	"""
	def __init__(self, backend: str = None):
		"""
		Creates a QMBackend object.

		Parameters
		----------
			backend : str, optional
				The name of the backend (simulator) to be used.

				Supported simulators are 'qulacs_gpu', 'qulacs','qibo', 'qiskit', 'cirq', 'pyquil'
				and 'symbolic'.
		"""
		self.backend = backend

	@property
	def backend(self):
		"""The name of the used backend (simulator)."""
		return self._backend

	@backend.setter
	def backend(self, backend: str = None):
		self._backend = tq.pick_backend(backend)
