import unittest
from quantmark import hello


class TestHello(unittest.TestCase):
	def test_returns_hello(self):
		self.assertEqual(hello(), "world")
