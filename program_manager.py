from tempfile import TemporaryDirectory

class ProgramManager:
    def __init__(self):
        self._temp_dir = TemporaryDirectory()
        self.program_list: list[str]
    
    def get_progrms(self):
        pass

    def write_programs(self):
        pass

    def print_options(self):
        pass