import unittest
from quantmark import circuit


class TestCircuit(unittest.TestCase):
	def test_validate_returns_true_on_valid_circuit(self):
		valid_circuit = """
			circuit: 
			X(target=(1,), control=(0,))
			Y(target=(1,), control=(0,))
			H(target=(0,))
			Phase(target=(0,), control=(1,), parameter=0.6366197723675814)
			Phase(target=(1,), control=(3,), parameter=a)
		"""
		result = circuit.validate_circuit_syntax(valid_circuit)
		self.assertEqual(result, True)

	def test_validate_returns_false_on_hello(self):
		result = circuit.validate_circuit_syntax('hello')
		self.assertEqual(result, False)

	def test_validate_returns_false_on_nonexistent_gate(self):
		nonvalid_circuit = """
			circuit:
			U(target=(1,), control=(0,))
		"""
		result = circuit.validate_circuit_syntax(nonvalid_circuit)
		self.assertEqual(result, False)

	def test_validate_returns_false_when_gate_has_wrong_properties(self):
		nonvalid_circuit = """
			circuit:
			X(target=(1,), control=(3,), parameter=a)
		"""
		result = circuit.validate_circuit_syntax(nonvalid_circuit)
		self.assertEqual(result, False)
