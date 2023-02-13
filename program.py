import requests
from os.path import join
from urllib.parse import urlparse

class Program:
    def __init__(self, download_link: str, program_name: str, temp_dir: str) -> None:
        self.download_link: str = download_link
        self.program_name: str = program_name
        self.temp_path: str = join(temp_dir, f"{program_name}_SETUP.exe")
        self._is_github_repo = "github" in self.download_link
    
    def __str__(self) -> str:
        if len(self.download_link) > 60:
            download_link = self.download_link
            download_link = download_link
        else:
            download_link = self.download_link
        return f"{self.program_name}: {download_link}"
    
    def install(self) -> None:
        """
        Called in order to install the program from the download link
        """
        print("Sending HTTP request...")

        if self._is_github_repo:
            # Check that the link is using the proper api
            if urlparse(self.download_link).netloc.startswith("api"):
                # Get the assets from the github api
                repo_assets = requests.get(self.download_link).json()["assets"]

                for asset in repo_assets:
                    if ".exe" in asset["name"]:
                        with open(self.temp_path, "wb") as file:
                            file.write(requests.get(asset["browser_download_url"]).content)
                        return
                    
                    elif "installer" in asset["name"].lower():
                        backup = asset
                
                with open(self.temp_path, "wb") as file:
                    file.write(requests.get(backup["browser_download_url"]).content)
            
            else:
                url_path = urlparse(self.download_link).path.split("/")

                repo_assets = requests.get(f"https://api.github.com/repos/{url_path[1]}/{url_path[2]}/releases/latest").json()["assets"]

                for asset in repo_assets:
                    if ".exe" in asset["name"]:
                        with open(self.temp_path, "wb") as file:
                            file.write(requests.get(asset["browser_download_url"]).content)
                        return
                    
                    elif "installer" in asset["name"].lower():
                        backup = asset

        try:
            req = requests.get(self.download_link)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
            print("Bad URL provided, check the url provided.")
        
        if not req.ok:
            print(f"Install attempt resulted in bad status code: {req.status_code} for program: {self.program_name}")
            return
        
        print("Request successful, now downloading installer...")
        with open(self.temp_path, "wb") as file:
            file.write(req.content)

if __name__ == "__main__":
    pass