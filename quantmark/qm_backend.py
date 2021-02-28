import tequila as tq


class QMBackend():
	"""
	Wrapper that makes sure the same backend is used and checks that it is
	available.
	"""
	def __init__(self, backend: str = None):
		"""
		Parameters
		----------
		backend: str, optional:
			Simulator name.
			Supported simulators: 'qulacs_gpu', 'qulacs','qibo', 'qiskit'
			'cirq', 'pyquil', 'symbolic'.
		"""
		self.backend = backend

	@property
	def backend(self):
		return self._backend

	@backend.setter
	def backend(self, backend: str = None):
		self._backend = tq.pick_backend(backend)

	def to_string(self):
		"""
		Returns a string that can be used to recreate the object with the
		QMBackend.fromString() method.
		"""
		return f'QMB;{self.backend}'

	@staticmethod
	def from_string(object_string: str):
		"""
		Used to recreate object from string.
		"""
		data = object_string.split(';')
		return QMBackend(*data[1:])
