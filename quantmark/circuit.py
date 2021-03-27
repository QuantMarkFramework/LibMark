from quantmark.create_multiline_regex import create_multiline_regex

NP_ONEQ_GATES_REGEX = "(X|Y|Z|H)\(target=\(\d+,\)(, control=\((\d+,|\d+(, \d+)+)\))?\)"
P_ONEQ_GATES_REGEX = "(Phase|Rx|Ry|Rz)\(target=\(\d+,\)(, control=\((\d+,|\d+(, \d+)+)\))?,"\
	" parameter=((\d+.\d*)|\D*)\)"
SWAP_GATE_REGEX = "SWAP\(target=\(\d*, \d*\)(, control=\((\d+,|\d+(, \d+)+)\))?\)"

def circuit_pattern():
	options = [NP_ONEQ_GATES_REGEX, P_ONEQ_GATES_REGEX, SWAP_GATE_REGEX]
	return create_multiline_regex(options, first_line='circuit:')

def validate_circuit_syntax(circuit: str) -> bool:
	return bool(circuit_pattern().match(circuit))
