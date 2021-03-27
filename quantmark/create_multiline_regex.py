import re
import typing as t

def create_multiline_regex(line: t.Union[str, t.List[str]], first_line: str = ''):
	if first_line:
		first_line = f'\s*{first_line}\s*(\r?\n)'
	if isinstance(line, list):
		options = '|'.join(line)
		line = f'({options})'
	if not isinstance(line, str):
		return None
	return re.compile(f'^{first_line}(\s*{line}\s*(\r?\n))*(\s*{line}\s*)$')
