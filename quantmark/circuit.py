import re
import typing
from dataclasses import dataclass
import tequila as tq
from quantmark.exceptions.same_control_and_target import SameControlAndTarget
from quantmark.exceptions.invalid_syntax_error import InvalidSyntaxError
from quantmark.create_multiline_regex import create_multiline_regex

NP_ONEQ_GATES_REGEX = "(X|Y|Z|H)\(target=\(\d+,\)(, control=\((\d+,|\d+(, \d+)+)\))?\)"
P_ONEQ_GATES_REGEX = "(Phase|Rx|Ry|Rz)\(target=\(\d+,\)(, control=\((\d+,|\d+(, \d+)+)\))?,"\
	" parameter=((\d+.\d*)|\D*)\)"
SWAP_GATE_REGEX = "SWAP\(target=\(\d*, \d*\)(, control=\((\d+,|\d+(, \d+)+|)\))?\)"

@dataclass
class GateDict:
	name: str
	target: typing.List[str]
	control: typing.List[str] = None
	parameter: typing.Union[str, float] = None

def circuit_pattern():
	options = [NP_ONEQ_GATES_REGEX, P_ONEQ_GATES_REGEX, SWAP_GATE_REGEX]
	return create_multiline_regex(options, first_line='circuit:')

def validate_circuit_syntax(circuit: str) -> bool:
	return bool(circuit_pattern().match(circuit))

def get_one_gate_data_from_string(string: str, data: str):
	target_area = string.split(f'{data}=(', 1)[1].split(")")[0]
	parts = target_area.split(',')
	if not parts[-1]:
		parts = parts[:-1]
	return [int(n) for n in parts]

def get_gate_parameter(string: str):
	string_patrameter = string.split("parameter=", 1)[1].split(")")[0]
	try:
		float_parameter = float(string_patrameter)
		return float_parameter
	except ValueError:
		return string_patrameter

def gate_string_to_dict(string: str):
	name = string.split("(", 1)[0]
	target = get_one_gate_data_from_string(string, 'target')
	control = None
	if 'control' in string:
		control = get_one_gate_data_from_string(string, 'control')
	parameter = None
	if 'parameter' in string:
		parameter = get_gate_parameter(string)
	return GateDict(name=name, target=target, control=control, parameter=parameter)

def gate_from_gate_dict(gate: GateDict):
	if gate.control and set(gate.target) & set(gate.control):
		raise SameControlAndTarget
	if gate.name in ['X', 'Y', 'Z', 'H']:
		gate_method = getattr(tq.gates, gate.name)
		return gate_method(target=gate.target, control=gate.control)
	if gate.name in ['Rx', 'Ry', 'Rz']:
		gate_method = getattr(tq.gates, gate.name)
		return gate_method(gate.parameter, target=gate.target, control=gate.control)
	if gate.name in ['Phase']:
		return tq.gates.Phase(phi=gate.parameter, target=gate.target, control=gate.control)
	if gate.name in ['SWAP']:
		first, second = gate.target
		return tq.gates.SWAP(first=first, second=second, control=gate.control)
	return None

def circuit_from_string(circuit: str):
	if not validate_circuit_syntax(circuit):
		raise InvalidSyntaxError
	gate_regex = re.compile(
		f'({NP_ONEQ_GATES_REGEX}|{P_ONEQ_GATES_REGEX}|{SWAP_GATE_REGEX})'
	)
	gates = gate_regex.findall(circuit)
	gates = [gate_string_to_dict(g[0]) for g in gates]
	if not gates:
		return None
	circuit = gate_from_gate_dict(gates[0])
	for gate in gates[1:]:
		circuit += gate_from_gate_dict(gate)
	return circuit
