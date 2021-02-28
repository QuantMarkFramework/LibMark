# pylint: disable=protected-access
import unittest
from quantmark import QMOptimizer


class TestQMOptimizer(unittest.TestCase):
	def test_to_string_and_bakc(self):
		original = QMOptimizer('scipy', 'BFGS', 'arg1', 'arg2', kwar='kwar', dar='dar')
		recreation = QMOptimizer.from_string(original.to_string())
		self.assertEqual(recreation._module, original._module)
		self.assertEqual(recreation._method, original._method)
		self.assertEqual(recreation._args, original._args)
		self.assertEqual(recreation._kwarks, original._kwarks)
