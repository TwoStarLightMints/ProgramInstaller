from tempfile import TemporaryDirectory

class ProgramManager:
    def __init__(self):
        self._temp_dir = TemporaryDirectory()