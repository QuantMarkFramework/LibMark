import tequila as tq

from deprecated import deprecated
from tequila.circuit import QCircuit as Circuit
from tequila import QubitHamiltonian
from quantmark.qm_backend import QMBackend as Backend
from quantmark.qm_optimizer import QMOptimizer as Optimizer
from quantmark.vqe.vqe_result import VQEResult as Result


@deprecated(reason="Use the VQEAlgorithm class with the analyze method instead.", action='always')
def vqe_benchmark(
	circuit: Circuit,
	optimizer: Optimizer = Optimizer(),
	backend: Backend = Backend(),
	molecule=None,
	hamiltonian: QubitHamiltonian = None,
	silent: bool = True,
	repetitions: int = 100,
	target_value: int = None
) -> Result:
	"""Deprecated. Use the VQEAlgorithm class with the analyze method instead."""
	if not molecule and not hamiltonian:
		raise Exception('You have give to a molecule or a hamiltonina')
	if molecule and hamiltonian:
		raise Exception('You have give to a molecule or a hamiltonina not both.')
	if molecule:
		objective = tq.ExpectationValue(H=molecule.make_hamiltonian(), U=circuit)
	if hamiltonian:
		objective = tq.ExpectationValue(H=hamiltonian, U=circuit)

	results = [None] * repetitions
	for i in range(repetitions):
		results[i] = optimizer.minimize(
			objective=objective,
			backend=backend.backend,
			silent=silent
		)
	test = Result(
		circuit,
		optimizer,
		backend,
		results,
		molecule=molecule,
		target_value=target_value,
		max_iterations=100
	)
	return test
