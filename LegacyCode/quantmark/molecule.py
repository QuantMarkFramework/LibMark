import re
import typing
import tequila as tq
from tequila.quantumchemistry.qc_base import QuantumChemistryBase
from quantmark.exceptions import InvalidSyntaxError, DuplicateValueError
from quantmark.create_multiline_regex import create_multiline_regex
from quantmark.decorators.cached import cached

SUPPORTED_ATOMS = [
	"H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al",
	"Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe",
	"Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr",
	"Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
	"Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", "Ir",
	"Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"
]


@cached
def geometry_pattern(compile: bool = True) -> typing.Union[typing.Pattern[str], str]:
	"""
	Creates a regex pattern for recognizing geometry strings.

	Parameters
	----------
		compile : bool
			If true the regex is compiled, otherwise it is returned as a string.

	Returns
	----------
	Returns a compiled pattern or string depending on the compile parameter.
	"""
	return create_multiline_regex(
		fr'(({"|".join(SUPPORTED_ATOMS)})( \d*\.?\d*){"{3}"})',
		compile=compile
	)


def validate_geometry_syntax(geometry: str) -> bool:
	"""
	Checks if the syntax of a string is valid so that it can be used to create a molecule.

	Parameters
	----------
		geometry : str
			The string representing the geometry.

			Example:\n
			H 0.0 0.0 0.0\n
			H 0.0 0.0 1.6

	Returns
	----------
	True when the geometry syntax is valid and false otherwise.
	"""
	return bool(geometry_pattern().match(geometry))


@cached
def orbitals_pattern(compile: bool = True) -> typing.Union[typing.Pattern[str], str]:
	"""
	Creates a regex pattern for recognizing strings containing orbitals.

	Parameters
	----------
		compile : bool
			If true the regex is compiled, otherwise it is returned as a string.

	Returns
	----------
	Returns a compiled pattern or string depending on the compile parameter.
	"""
	return create_multiline_regex(orbital_pattern(compile=False), compile=compile)


@cached
def orbital_pattern(compile: bool = True) -> typing.Union[typing.Pattern[str], str]:
	"""
	Creates a regex pattern for recognizing orbital strings.

	Parameters
	----------
		compile : bool
			If true the regex is compiled, otherwise it is returned as a string.

	Returns
	----------
	Returns a compiled pattern or string depending on the compile parameter.
	"""
	regex_string = r"([A-Q]\d( \d+)+)"
	if compile:
		return re.compile(regex_string)
	return regex_string


def validate_orbitals_syntax(orbitals: str) -> bool:
	"""
	Checks if the syntax of a string is valid so that it can be used to create a molecule.

	Parameters
	----------
		orbitals : str
			The string representing the orbitals.

			Example:\n
			A1 1 2 3\n
			B0 4 5

	Returns
	----------
	True when the orbitals syntax is valid and false otherwise.
	"""
	return bool(orbitals_pattern().match(orbitals))


def orbitals_from_string(orbitals: str) -> dict:
	"""
	Takes in a string representating orbitals and returns a corresponding dict that can be used in
	tequila.Molecule to create a molecule.

	Parameters
	----------
		orbitals : str
			The string representing the orbitals.

			Example:\n
			A1 1 2 3\n
			B0 4 5

	Returns
	----------
	A dict that can be used as the orbitals argument in tequila.Molecule.
	"""
	if not validate_orbitals_syntax(orbitals):
		raise InvalidSyntaxError
	parts = orbital_pattern().findall(orbitals)
	orbitals_dictionary = {}
	for part, _ in parts:
		metrics = part.split()
		if metrics[0] in orbitals_dictionary:
			raise DuplicateValueError
		orbitals_dictionary[metrics[0]] = [int(i) for i in metrics[1:]]
	return orbitals_dictionary


def create(
	geometry: str,
	basis_set: str = None,
	active_orbitals: typing.Union[dict, list, str] = None,
	transformation: typing.Union[str, typing.Callable] = None,
	backend: str = None,
	guess_wfn=None,
	*args,
	**kwargs
) -> QuantumChemistryBase:
	"""
	Uses the tequila.chemistry.Molecule function to create molecule
	object. Only difference is that active orbitals can be given as
	string.
	"""
	if isinstance(active_orbitals, str):
		active_orbitals = orbitals_from_string(active_orbitals)
	return tq.chemistry.Molecule(
		geometry=geometry,
		basis_set=basis_set,
		active_orbitals=active_orbitals,
		transformation=transformation,
		backend=backend,
		guess_wfn=guess_wfn,
		*args,
		**kwargs
	)
