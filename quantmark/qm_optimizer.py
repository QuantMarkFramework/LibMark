

class QMOptimizer:
	"""
	A class that holds information about a optimizer and can be given as a parameter to an
	algorithm.

	Optimizing means minimizing in this case.

	Methods
	-------
		minimize(objective, backend=None, silent=True):
			Runs the optimizer on a given objective.
	"""
	def __init__(self, module: str = "scipy", method: str = "BFGS", *args, **kwarks):
		"""
		Creates a QMOptimizer object.

		Parameters
		----------
			module : str
				The module from which the optimizer (minimize) method should be used.

				Supported modules are 'scipy', 'gd', 'gpyopt' and 'phoenics'.
			method : str
				The method to be used from the module.
			*args :
				Additional arguments to be passed to the module.
			**kwarks :
				Additional key arguments to be passed to the module.
		"""
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

	def minimize(self, objective, backend: str = None, silent: bool = True):
		"""
			Runs the optimizer on a given objective.

		Parameters
		----------
			objective :
				The objective to be minimized.
			backend : str
				The backend (simulator) to be used.
			silent : bool
				If True the minimizing process will not print information while it is running.

		Returns
		----------
		The result from the minimizing process.
		"""
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
