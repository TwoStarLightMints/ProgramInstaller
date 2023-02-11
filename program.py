import requests
from os.path import join

class Program:
    def __init__(self, download_link: str, program_name: str, temp_dir: str) -> None:
        self.download_link: str = download_link
        self.program_name: str = program_name
        self.temp_path: str = join(temp_dir, f"{program_name}_SETUP.exe")
    
    def __str__(self) -> str:
        if len(self.download_link) > 60:
            download_link = self.download_link[:60]
            download_link = download_link + "..."
        else:
            download_link = self.download_link
        return f"{self.program_name}: {download_link}"
    
    def install(self) -> None:
        """
        Called in order to install the program from the download link
        """
        print("Sending HTTP request...")
        try:
            req = requests.get(self.download_link)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
            print("Bad URL provided, check the url provided.")

        
        if not req.ok:
            print(f"Install attempt resulted in bad status code: {req.status_code}")
            return
        
        print("Request successful, now downloading installer...")
        with open(self.temp_path, "wb") as file:
            file.write(req.content)

if __name__ == "__main__":
    pass