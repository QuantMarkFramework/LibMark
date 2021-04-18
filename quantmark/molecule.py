""" Molecule

Some extra functionality to handle molecules.

The create function uses the tequila.chemistry.Molecule function to create a
molecule object. Only difference is that active_orbitals can be given as
string.
"""

import functools
import re
import typing
import tequila as tq
from tequila.quantumchemistry.qc_base import QuantumChemistryBase
from quantmark.exceptions import InvalidSyntaxError, DuplicateValueError
from quantmark.create_multiline_regex import create_multiline_regex

SUPPORTED_ATOMS = [
	"H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al",
	"Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe",
	"Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr",
	"Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
	"Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", "Ir",
	"Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"
]


@functools.lru_cache()
def geometry_pattern(compile: bool = True):
	return create_multiline_regex(
		fr'(({"|".join(SUPPORTED_ATOMS)})( \d*\.?\d*){"{3}"})',
		compile=compile
	)


def validate_geometry_syntax(geometry: str) -> bool:
	"""
	Syntax:
		H 0.0 0.0 0.0
		Li 0.0 0.0 1.6
	"""
	return bool(geometry_pattern().match(geometry))


@functools.lru_cache()
def orbitals_pattern(compile: bool = True):
	"""
	Syntax:
		A1 1 2 4 5 7
		B1 0 2
	"""
	return create_multiline_regex(orbital_pattern(compile=False), compile=compile)


@functools.lru_cache()
def orbital_pattern(compile: bool = True):
	"""
	Syntax:
		A1 1 2 3
	"""
	regex_string = r"([A-Q]\d( \d+)+)"
	if compile:
		return re.compile(regex_string)
	return regex_string


def validate_orbitals_syntax(orbitals: str) -> bool:
	return bool(orbitals_pattern().match(orbitals))


def orbitals_from_string(orbitals: str) -> dict:
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
