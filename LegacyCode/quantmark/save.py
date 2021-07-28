import os
import csv
import typing
import time
import datetime

from quantmark.vqe.vqe_result import VQEResult


def create_molecular_formula(atoms: typing.List[str]) -> str:
	"""
	Creates a molecular formula out of a list of moleules:

	Parameters
	----------
		atoms : List[str]
			A list of atoms. Example: ['H', 'O', 'H']

	Returns
	----------
	A molecular formula. Example: 'H2O'
	"""
	dictionary = {}
	for atom in atoms:
		if atom not in dictionary:
			dictionary[atom] = 1
			continue
		dictionary[atom] += 1
	string = ""
	for i in sorted(dictionary.keys()):
		string += i
		if dictionary[i] > 1:
			string += str(dictionary[i])
	return string


def geometry_to_xyz(geometry: list) -> str:
	"""
	Creates a string with the .xyz format from a list that represents the geometry

	Parameters
	----------
		geometry : list
			A list returned representing the geometry. Example:
			[('H', (0.0, 0.0, 0.0)), ('H', (0.0, 0.0, 1.6))]

	Returns
	----------
	A string with the .xyz format. Example: '2\n\nH  0.0  0.0  0.0\nH  0.0  0.0  0.6'
	"""
	strings = []
	strings.append(str(len(geometry)) + "\n")
	for atom in geometry:
		string = atom[0] + "  "
		string += str(atom[1][0]) + "  "
		string += str(atom[1][1]) + "  "
		string += str(atom[1][2])
		strings.append(string)
	return "\n".join(strings)


def create_data_row(result: VQEResult) -> typing.List[str]:
	"""
	Creates a fata row with information about the reusl to be saved in a csv file.

	Parameters
	----------
		result : VQEResult
			The result class given by VQEAlgorithm.analyze().

	Returns
	----------
	A list with Qubit Count, Gate Depth, Gate Count, Parameter Count, Average Iterations,
	Success Rate, Molecular Formula, Basis Set, Transformation, Optimizer Module, Optimizer Method,
	Backend and Iteration Limit.
	"""
	return [
		result.qubit_count,
		result.gate_depth,
		result.gate_count,
		result.parameter_count,
		result.average_iterations,
		result.success_rate,
		create_molecular_formula(result.molecule.molecule.atoms),
		result.molecule.molecule.basis,
		result.molecule.transformation._trafo.__name__,
		result.optimizer.module,
		result.optimizer.method,
		result.backend.backend,
		result.iteration_limit
	]


def save(result: VQEResult, algorithm_name: str = "undefined") -> None:
	"""
	Saves data about the algorithm.

	One 'experiments.csv' contains data about all experiments. Additional information can be found
	in a folder corresponding to the algorithm name.

	Parameters
	----------
		result : VQEResult
			The result class given by VQEAlgorithm.analyze() that contains the data you want to save.
		algorithm_name: str
			A name that is saved as the name of the algorithm. All the experiments with the same
			algorithm name are saaved in the same folder.
	"""
	molecular_formula = create_molecular_formula(result.molecule.molecule.atoms)
	data_row = create_data_row(result)

	if not os.path.exists(algorithm_name):
		os.mkdir(algorithm_name)

	time_string = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
	experiment_name = molecular_formula + "-" + time_string

	os.mkdir(os.path.join(algorithm_name, experiment_name))

	experiment_path = os.path.join(algorithm_name, experiment_name, 'experiment.csv')
	with open(experiment_path, 'x', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([
			"Qubit Count",
			"Gate Depth",
			"Gate Count",
			"Parameter Count",
			"Average Iterations",
			"Success Rate",
			"Molecular Formula",
			"Basis Set",
			"Transformation",
			"Optimizer Module",
			"Optimizer Method",
			"Backend",
			"Iteration Limit"
		])
		writer.writerow(data_row)

	iterations_path = os.path.join(algorithm_name, experiment_name, 'iterations.csv')
	with open(iterations_path, 'x', newline='') as file:
		writer = csv.writer(file)
		columns = result.max_iterations
		writer.writerow([f'Iteration {i}' for i in range(1, columns + 1)])
		for res in result.results:
			history = res.history.energies.copy()
			while len(history) < columns:
				history.append(None)
			writer.writerow(history)

	geometry_path = os.path.join(algorithm_name, experiment_name, 'geometry.xyz')
	with open(geometry_path, 'x', newline='') as file:
		file.write(geometry_to_xyz(result.molecule.molecule.geometry))

	if not os.path.isfile('experiments.csv'):
		with open('experiments.csv', 'x', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([
				"Qubit Count",
				"Gate Depth",
				"Gate Count",
				"Parameter Count",
				"Average Iterations",
				"Success Rate",
				"Molecular Formula",
				"Basis Set",
				"Transformation",
				"Optimizer Module",
				"Optimizer Method",
				"Backend",
				"Iteration Limit",
				"Algorithm Name",
				"Experiment Name",
			])

	with open('experiments.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		full_data_row = data_row.copy()
		full_data_row.append(algorithm_name)
		full_data_row.append(experiment_name)
		writer.writerow(full_data_row,)
	return
