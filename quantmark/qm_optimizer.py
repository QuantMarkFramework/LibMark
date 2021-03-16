import json

class QMOptimizer:
	"""
	Wrapper that makes sure the same method for optimizing is used.
	"""
	def __init__(self, module: str = "scipy", method: str = "BFGS", *args, **kwarks):
		if isinstance(module, str):
			if module == "scipy":
				from tequila.optimizers.optimizer_scipy import minimize
				self._minimize = minimize
			elif module == 'gd':
				from tequila.optimizers.optimizer_gd import minimize
				self._minimize = minimize
			elif module == 'gpyopt':
				from tequila.optimizers.optimizer_gpyopt import minimize
				self._minimize = minimize
			elif module == 'phoenics':
				from tequila.optimizers.optimizer_phoenics import minimize
				self._minimize = minimize
		self._module = module
		self._method = method
		self._args = args
		self._kwarks = kwarks

	def minimize(self, objective, backend=None, silent=True):
		return self._minimize(
			objective=objective,
			method=self._method,
			gradient=None,
			hessian=None,
			initial_values=None,
			variables=None,
			backend=backend,
			silent=silent,
			tol=1.e-13,
			*self._args,
			**self._kwarks
		)

	def to_string(self):
		"""
		Returns a string that can be used to recreate the object with the
		QMOptimizer.from_string() method.
		"""
		args = ";" + ";".join(self._args) if self._args else ""
		kwarks = "KW" + json.dumps(self._kwarks) if self._kwarks else ""
		return f'QMO;{self._module};{self._method}{args}{kwarks}'

	@staticmethod
	def from_string(object_string: str):
		"""
		Used to recreate object from string.
		"""
		data_kwarks = object_string.split('KW')
		data = data_kwarks[0].split(';')
		kwarks = json.loads(data_kwarks[1]) if data_kwarks[1] else {}
		return QMOptimizer(*data[1:], **kwarks)
