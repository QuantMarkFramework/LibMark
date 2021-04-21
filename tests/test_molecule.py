import unittest
from quantmark import molecule


class TestMolecule(unittest.TestCase):
	def test_validate_geometry_returns_true_on_valid(self):
		geometry = """
			H 0.0 0.0 0.0
			Li 0.0 0.0 1.6
		"""
		self.assertTrue(molecule.validate_geometry_syntax(geometry))

	def test_validate_geometry_returs_false_on_moi(self):
		self.assertFalse(molecule.validate_geometry_syntax('moi'))

	def test_validate_geometry_returns_true_on_long_linebreak(self):
		geometry = 'H 0.0 0.0 0.0\r\nLi 0.0 0.0 1.6'
		self.assertTrue(molecule.validate_geometry_syntax(geometry))

	def test_validate_orbitals_orbitals_true_on_valid(self):
		orbitals = """
			A1 1 2
			B2 4 5
		"""
		self.assertTrue(molecule.validate_orbitals_syntax(orbitals))

	def test_validate_orbitals_return_false_on_moi(self):
		self.assertFalse(molecule.validate_orbitals_syntax('moi'))

	def test_validate_orbitals_returns_true_on_long_linebreaks(self):
		orbitals = 'A1 1 2\r\nB2 4 5'
		self.assertTrue(molecule.validate_orbitals_syntax(orbitals))

	def test_orbitals_from_string_returns_correct_dict(self):
		result = molecule.orbitals_from_string('A1 1 2\nB2 4 5')
		target_result = {'A1': [1, 2], 'B2': [4, 5]}
		self.assertEqual(result, target_result)
