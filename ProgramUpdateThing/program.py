import win32.win32api
import requests



class Program:
    
    def __init__ (self, file_path: str, program_name: str, download_link: str, temp_store: str):
        
        # File path to client executable
        self.file_path: str = file_path
        # Name of the program
        self.program_name: str = program_name
        # Download link for the program, where the setup executable will be downloaded from
        self.download_link: str = download_link
        # Use get_version_number to retrieve version info from executable by passing in the client executable file path
        self.client_version: str = self.get_version_number(self.file_path)
        # Use the temporary directory, program name (cleaned for creation of executable), and exe suffix to create the setup executable which will be used to check against the client executable
        self.setup_exe_path: str = temp_store + "\\" + self._NAME_clean(program_name) + ".exe"
        # Use the download link to navigate to the webpage to download the binary file, pass in the executable path to give the location to download the file to
        self.get_executable(self.download_link, self.setup_exe_path)
        # Get the version information of the up to date setup executable by passing in the setup executable path created before
        self.server_version: str = self.get_version_number(self.setup_exe_path)
        # Whether a program is up to date or not
        self.up_to_date: bool = self.client_version == self.server_version

    
    # Used in ProgramManager class for printing of the programs in a succint manner
    def __str__(self) -> str:
        return f"{self.program_name}\n\t( File path: {self.file_path} | Download link: {self.download_link} | {self.check_updatedness()} )"


    # Uses a geek for geeks solution to finding version info using win32api
    def get_version_number (self, current_file_path: str) -> str:
        File_information = win32.win32api.GetFileVersionInfo(current_file_path, "\\")
    
        ms_file_version = File_information['FileVersionMS']
        ls_file_version = File_information['FileVersionLS']

        return f'{str(win32.win32api.HIWORD(ms_file_version))}.{str(win32.win32api.LOWORD(ms_file_version))}.{str(win32.win32api.HIWORD(ls_file_version))}.{str(win32.win32api.LOWORD(ls_file_version))}'


    # Sends a get request to the download link given by the user to retrieve the binary data, then write that data to the created save path
    def get_executable (self, download_link: str, save_path: str) -> None:
        r = requests.get(download_link, allow_redirects=True)
        with open(save_path, 'wb') as dest:
            dest.write(r.content)


    # Compares the server and client versions of the executables in order to give the proper output when printing the program object, indicating up to dateness
    def check_updatedness (self) -> str:
        return "--UP TO DATE--" if self.server_version == self.client_version else "--OUT OF DATE--"
    

    # Removes spaces and turns any letters to lowercase for uniform executable names
    def _NAME_clean (self, name: str) -> str:
        return "".join(name.lower().split(" "))

def get_version_number (current_file_path: str) -> str:
        File_information = win32.win32api.GetFileVersionInfo(current_file_path, "\\")
    
        ms_file_version = File_information['FileVersionMS']
        ls_file_version = File_information['FileVersionLS']

        return f'{str(win32.win32api.HIWORD(ms_file_version))}.{str(win32.win32api.LOWORD(ms_file_version))}.{str(win32.win32api.HIWORD(ls_file_version))}.{str(win32.win32api.LOWORD(ls_file_version))}'

if __name__ == "__main__":
  pass