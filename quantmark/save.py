import os
import csv
import typing
import time
import datetime
from quantmark.vqe.vqe_result import VQEResult


def create_molecular_formula(atoms: typing.List[str]) -> str:
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
	strings = []
	strings.append(str(len(geometry)) + "\n")
	for atom in geometry:
		string = atom[0] + "  "
		string += str(atom[1][0]) + "  "
		string += str(atom[1][1]) + "  "
		string += str(atom[1][2])
		strings.append(string)
	return "\n".join(strings)


def create_data_row(result):
	return [
		result.qubit_count,
		result.gate_depth,
		result.gate_count,
		result.parameter_count,
		result.average_iterations,
		result.success_rate,
		create_molecular_formula(result.molecule.molecule.atoms),
		result.molecule.molecule.basis,
		result.molecule.transformation._trafo.__name__
	]


def save(result: VQEResult, algorithm_name: str = "Undefined") -> None:
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
			"Transformation"
		])
		writer.writerow(data_row)

	iterations_path = os.path.join(algorithm_name, experiment_name, 'iterations.csv')
	with open(iterations_path, 'x', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([f'Iteration {i}' for i in range(1, result.max_iterations + 1)])
		for res in result.results:
			history = res.history.energies.copy()
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
				"Algorithm Name",
				"Experiment Name",
			])

	with open('experiments.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		full_data_row = data_row.copy()
		full_data_row.append(algorithm_name)
		full_data_row.append(experiment_name)
		writer.writerow(full_data_row)
	return
