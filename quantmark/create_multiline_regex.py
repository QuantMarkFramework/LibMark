import re
import typing as t


def create_multiline_regex(
	line: t.Union[str, t.List[str]],
	first_line: str = '',
	compile: bool = True
) -> t.Union[t.Pattern[str], str]:
	"""
	Creates a regex pattern that has many same lines. Ignores some white space between lines.

	Parameters
	----------
		line : str, List[str]
			The pattern or the patterns that are accepted lines.
		first_line : str
			A special pattern that can be given for and only for the first line.
		compile : bool
			If true the regex is compiled, otherwise it is returned as a string.

	Returns
	----------
	Returns a compiled pattern or string depending on the compile parameter.
	"""
	if first_line:
		first_line = fr'\s*{first_line}\s*(\r?\n)'
	if isinstance(line, list):
		options = '|'.join(line)
		line = fr'({options})'
	if not isinstance(line, str):
		return None
	regex_string = fr'^{first_line}(\s*{line}\s*(\r?\n))*(\s*{line}\s*)$'
	if compile:
		return re.compile(regex_string)
	return regex_string
