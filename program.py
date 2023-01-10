import requests
from os.path import join

class Program:
    def __init__(self, download_link: str, program_name: str, temp_dir: str) -> None:
        self.download_link: str = download_link
        self.program_name: str = program_name
        self.temp_path: str = join(temp_dir, f"{program_name}.exe")
    
    def install(self) -> int:
        """
        Called in order to install the program from the download link
        """
        print("Sending HTTP request...")
        req = requests.get(self.download_link)
        
        if not req.ok:
            print(f"Install attempt resulted in bad status code: {req.status_code}")
            return INSTALLER_ENUM_HERE
        
        print("Request successful, now downloading installer...")
        with open(self.temp_path, "wb") as file:
            file.write(req.content)

        return INSTALLER_ENUM_HERE