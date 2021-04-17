import unittest
import tequila as tq
from quantmark import circuit

VALID_CIRCUIT_STRING = """
			circuit: 
			X(target=(1,), control=(0,))
			Y(target=(1,), control=(0,))
			H(target=(0,))
			Phase(target=(0,), control=(1,), parameter=0.6366197723675814)
			Phase(target=(1,), control=(3,), parameter=a)
		"""

valid_circuit = tq.gates.Ry(angle='a', target=0)
valid_circuit += tq.gates.Phase(angle=2, target=2, control=1)
valid_circuit += tq.gates.SWAP(first=1, second=2)
valid_circuit += tq.gates.Ry(angle='a', target=0)
valid_circuit += tq.gates.H(target=1, control=2)
valid_circuit += tq.gates.Ry(angle='b', target=0)

class TestCircuit(unittest.TestCase):
	def test_validate_returns_true_on_valid_circuit(self):
		result = circuit.validate_circuit_syntax(VALID_CIRCUIT_STRING)
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

	def test_no_control_swap_gate_validation(self):
		problematic_circuit = """
			circuit: 
			Ry(target=(0,), parameter=a)
			Phase(target=(2,), control=(1,), parameter=2.0)
			SWAP(target=(1, 2), control=())
			H(target=(1,), control=(2,))
		"""
		result = circuit.validate_circuit_syntax(problematic_circuit)
		self.assertTrue(result)

	def test_circuit_print_creates_same_circuit(self):
		string = valid_circuit.__str__()
		print(string)
		new_circuit = circuit.circuit_from_string(string)
		self.assertEqual(new_circuit, valid_circuit)

	def test_long_line_break_validation(self):
		test_circuit = 'circuit:\r\nX(target=(1,), control=(3,))'
		result = circuit.validate_circuit_syntax(test_circuit)
		self.assertTrue(result)

	def test_circuit_info_returns_right_qubit_count(self):
		info = circuit.CircuitInfo(valid_circuit)
		self.assertEqual(info.qubit_count, 3)

	def test_circuit_info_returns_right_gate_depth(self):
		info = circuit.CircuitInfo(valid_circuit)
		self.assertEqual(info.gate_depth, 3)

	def test_circuit_info_returns_right_gate_count(self):
		info = circuit.CircuitInfo(valid_circuit)
		self.assertEqual(info.gate_count, 6)

	def test_circuit_info_returns_right_parameter_count(self):
		info = circuit.CircuitInfo(valid_circuit)
		self.assertEqual(info.parameter_count, 2)
