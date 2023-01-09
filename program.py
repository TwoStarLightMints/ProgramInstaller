import requests

class Program:
    def __init__(self, download_link, program_name) -> None:
        self.download_link: str = download_link
        self.program_name: str = program_name
    
    def install(self) -> int:
        """
        Called in order to install the program from the download link
        """
        req = requests.get(self.download_link)
        
        if not req.ok:
            print(f"Install attempt resulted in bad status code: {req.status_code}")
            return 1
        