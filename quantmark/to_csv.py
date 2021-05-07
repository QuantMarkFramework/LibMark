import csv
import typing
from quantmark.vqe.vqe_result import VQEResult


def create_molecular_formula(atoms: typing.List[str]) -> str:
	dictionary = {}
	for atom in atoms:
		if not atom in dictionary:
			dictionary[atom] = 1
			continue
		dictionary[atom] += 1
	string = ""
	for i in sorted(dictionary.keys()):
		string += i
		if dictionary[i] > 1:
			string += str(dictionary[i])
	return string

def geometry_to_string(geometry: list) -> str:
	strings = []
	for atom in geometry:
		string = atom[0] + " "
		string += str(atom[1][0]) + " "
		string += str(atom[1][1]) + " "
		string += str(atom[1][2])
		strings.append(string)
	return "\n".join(strings)

def create_molecule_data(molecule) -> typing.List[str]:
	molecular_formula = create_molecular_formula(molecule.molecule.atoms)
	geometry = geometry_to_string(molecule.molecule.geometry)
	basis_set = molecule.molecule.basis
	transformation = molecule.transformation._trafo.__name__
	return [molecular_formula, geometry, basis_set, transformation]

def to_csv(result: VQEResult) -> None:
	with open('experiment.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Molecular Formula", "Geometry", "Basis set", "Transformation"])
		writer.writerow(create_molecule_data(result.molecule))
		writer.writerow([
			"Qubit count",
			"Gate depth",
			"Gate count",
			"Parameter count",
			"Average Iterations",
			"Success rate"
		])
		writer.writerow([
			result.qubit_count,
			result.gate_depth,
			result.gate_count,
			result.parameter_count,
			result.average_iterations,
			result.success_rate
		])
		writer.writerow([f'Iteration {i}' for i in range(1, result.max_iterations + 1)])
		for res in result.results:
			history = res.history.energies.copy()
			writer.writerow(history)
	return

if __name__=="__main__":
	print(create_molecular_formula(["C", "B", "A"]))
	print(create_molecular_formula(["A", "C", "B"]))
	print(create_molecular_formula(["Ai", "C", "Ai"]))