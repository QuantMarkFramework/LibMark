import re
import typing as t

def create_multiline_regex(
	line: t.Union[str, t.List[str]],
	first_line: str = '',
	compile: bool = True
	):
	if first_line:
		first_line = f'\s*{first_line}\s*(\r?\n)'
	if isinstance(line, list):
		options = '|'.join(line)
		line = f'({options})'
	if not isinstance(line, str):
		return None
	regex_string = f'^{first_line}(\s*{line}\s*(\r?\n))*(\s*{line}\s*)$'
	if compile:
		return re.compile(regex_string)
	return regex_string
