from src.utils.file_reader import FileReader

class Script:
    def __init__(self, description: str, path: str):
        self.description = description
        self.path = path

    def __str__(self) -> str:
        return FileReader.read(self.path)