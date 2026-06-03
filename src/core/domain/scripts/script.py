import re

from common.utils.file_reader import FileReader

class Script:
    def __init__(self, description: str, path: str, variables: dict[str, str] = {}):
        self.description = description
        self.path = path
        self.variables = variables

    def __str__(self) -> str:
        if self.variables:
            js = FileReader.read(self.path)

            def replace_placeholder(match: re.Match[str]) -> str:
                var_name = match.group(1)
                return str(self.variables.get(var_name, 'false'))

            js = re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", replace_placeholder, js)

            return js

        return FileReader.read(self.path)