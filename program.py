class Program:
    def __init__(self, download_link, program_name) -> None:
        self.download_link: str = download_link
        self.program_name: str = program_name
    
    def install() -> int:
        """
        Called in order to install the program from the download link
        """
        pass