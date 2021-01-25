from quantmark import hello
import unittest

class TestHello(unittest.TestCase):
	def test_returns_hello(self):
		self.assertEqual(hello(), "world")
