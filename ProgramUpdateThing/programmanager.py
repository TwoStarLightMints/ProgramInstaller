import os
import csv
from time import sleep
from tempfile import TemporaryDirectory
from linkcleaner import LinkCleaner
from program import Program
from subprocess import run
from requests import get



class ProgramManager:
    # The folder path for the folder which holds the program object storage file
    _PROGRAMS_FOLDER_PATH: str = "./programs_folder/"
    # Defines the path for the program object storage file
    _PROGRAMS_FILE_PATH: str = _PROGRAMS_FOLDER_PATH + "programs.csv"
    # Folder which will hold the chosen executables to use
    _SETUP_STORE_PATH: str = "./steups_to_use/"
    # Flag marking whether the program storage file requires updating
    _INFO_ALTERED: bool = False

    def __init__(self):
        # Create the temporary directory to hold the setup executables for checking up to dateness
        self._temp_setup_exe_location = TemporaryDirectory()
        # The list of programs which will be in use during the program
        self.program_list = self.retrieve_programs()
        # Used in the main loop to quit or continue running
        self.running = True

        self.run()
    
    # Retrieve all currently saved programs, or return an empty program object list
    def retrieve_programs (self) -> list[Program]:
        programs: list[Program] = []
        # If a program object storage file exists
        if os.path.isfile(self._PROGRAMS_FILE_PATH):
            # Read all the lines from the csv file and create program objects to add to the program object list to be used during runtime
            with open(self._PROGRAMS_FILE_PATH, newline='') as prog_file:
                reader = csv.reader(prog_file, delimiter=',', quotechar='|')
                for row in reader:
                    # Each row is a list
                    programs.append(Program(row[1], row[0], row[2], self._temp_setup_exe_location.name))
            return programs

        else:
            # Otherwise, return an empty list which will be updated during runtime
            return programs

    # Save the currently loaded program objects to the program storage file
    def write_programs (self):
        print("saving to file...")
        # The the program storage area does not exist, then create it
        if not os.path.isdir(self._PROGRAMS_FOLDER_PATH):
            os.mkdir(self._PROGRAMS_FOLDER_PATH)
        
        # Write the information stored by the programs which will be later used to instanciate program objects using this stored data
        with open(self._PROGRAMS_FILE_PATH, 'w', newline='') as prog_file:
            writer = csv.writer(prog_file, delimiter=',', quotechar='|')
            for program in self.program_list:
                writer.writerow([program.program_name, program.file_path, program.download_link])
    
    # Use the __str__ method of each program object stored in the program list to print each program to the console
    def view_programs (self) -> None:
        if len(self.program_list) != 0:
            for program in self.program_list:
                print(program)
        else:
            print("--NO PROGRAMS CURRENTLY STORED--")
        input("Hit enter to continue...")
    
    # Get input from the user and then pass it to the program class's constuructor method, then add the newly created program object to the program list, then change the altered flag to true so that the program knows to rewrite the program storage file
    def create_program (self) -> None:
        program_name = input("Enter the name of the program: ")
        file_path = input(f"Enter the path to {program_name}: ")
        download_link = input(f"Enter the download link for {program_name}: ")
        
        link_clean = LinkCleaner(download_link)
        
        self.program_list.append(Program(file_path, program_name, link_clean.clean_link, self._temp_setup_exe_location.name))
        self._INFO_ALTERED = True
    
    def get_executable (self, download_link: str, save_path: str) -> None:
        r = get(download_link, allow_redirects=True)
        with open(save_path, 'wb') as dest:
            dest.write(r.content)

    def create_program_and_install (self) -> None:
        program_name = input("Enter the name of the program: ")
        download_link = input(f"Enter the download link for {program_name}: ")

        clean_name = "".join(program_name.lower().split(" "))
        clean_link = LinkCleaner(download_link).clean_link

        agree = input(f"Download and setup of {program_name} will begin, proceed? (y/n) ")

        if agree == "y":
            input(f"During installation process, please remember to copy or take note of the path to {program_name}'s executable file. (Hit 'enter' to continue)")
            setup_download_location = TemporaryDirectory()
            self.get_executable(clean_link, setup_download_location.name + "\\" + clean_name + ".exe")
            print(setup_download_location.name + "\\" + clean_name)
            run(setup_download_location.name + "\\" + clean_name + ".exe")
            installed_program_exe_path = input(f"Enter the executable path for the recently installed {program_name}: ")

            self.program_list.append(Program(installed_program_exe_path, program_name, clean_link, self._temp_setup_exe_location.name))
            setup_download_location.cleanup()

            print(f"{program_name} has been successfully installed and added to the list of programs. Now returning to main menu...")
            sleep(3)

        else:
            print("Program creation aborted. Returning to main menu...")
            sleep(3)
    
    def choose_program_by_number (self, prompt: str) -> int:
        i = 1
        for program in self.program_list:
            print(f"{i}. {program.program_name}")
            i += 1
        
        return int(input(prompt)) - 1

    # Remove a program using its index in the program list, change the altered flag to true so that the program knows to rewrite the program storage file
    def remove_program (self) -> None:
        index = self.choose_program_by_number("Enter the number of the program you wish to remove: ")
        del self.program_list[index]
        self._INFO_ALTERED = True
    
    # Change information within an already create program object
    def edit_program (self) -> None:
        index = self.choose_program_by_number("Enter the number of the program you wish to edit: ")
        
        os.system("cls")
        
        chosen_program = self.program_list[index]
        print(chosen_program)
        
        field = input("What field would you like to edit? \n(1. Program Name) (2. File Path) (3. Download Link)\n(Enter the number of the field you would like to edit): ")
        
        if field == "1":
            chosen_program.program_name = input("Input the new program name: ")
        elif field == "2":
            chosen_program.file_path = input("Input the new file path: ")
        elif field == "3":
            chosen_program.download_link = input("Input the new download link: ")
        else:
            print("Invalid index")
            return
        
        self._INFO_ALTERED = True
    
    def update_programs (self) -> None:
        agree = input("You are about to update all the currently out of date programs, proceed? (y/n): ")

        if agree == "y":
            for program in self.program_list:
                if not program.up_to_date:
                    run(program.setup_exe_path)
            
            print("All programs up to date. Now returning to main menu...")
            sleep(3)
    
    def update_select_programs (self) -> None:
        index = self.choose_program_by_number("Please enter the number of the program you would like to update: ")
        
        run(self.program_list[index].setup_exe_path)
    
    def provide_help (self) -> None:
        print("Welcome to the update thing, there is no name for it right now, it doesn't matter")
        print("When you first opened this program, a folder was made in whatever directory you have this script which contains a csv file which holds the data for each program.")
        print("The csv file contains/will contain the program names, file paths (to the executable file of the program which is stored in your computer), and the download links for the programs you have entered.")
        print("You can view all the programs which are stored in this program by entering '1' on the options screen, you can add a program by entering '2', you can remove a program by entering '3', or you can edit a program by entering '4'.")
        print("To quit the program, when you are on the options screen, enter 'q'.")
        print("If you have any other questions or things that I can add to this to make it better, just text me.")
        input("Hit enter to continue...")
    
    def quit_program (self):
        self.running = False
    
    # Prints the options for the user to the screen
    def print_options (self) -> None:
        print("1. View a list of the programs.")
        print("2. Create a new program and add it to the list.")
        print("3. Remove a program from the list.")
        print("4. Edit the contents of a program.")
        print("5. Update all out of date programs.")
        print("6. Update a select program.")
        print("7. Create a new program, install it, and add it to the list.")
        print("Press h and hit 'enter' for help")
        print("Press q and hit 'enter' to quit")

    # Uses a dict to store the different option numbers and methods, uses a user input argument as the selector
    def select_option (self, selection: str) -> None:
        os.system('cls')
        choices_dict = {
            "1": self.view_programs,
            "2": self.create_program,
            "3": self.remove_program,
            "4": self.edit_program,
            "5": self.update_programs,
            "6": self.update_select_programs,
            "7": self.create_program_and_install,
            "h": self.provide_help,
            "q": self.quit_program
        }

        choices_dict.get(selection.lower())()

    # The main method of the class and main loop
    def run (self) -> None:
        
        while self.running:
            
            os.system('cls')
            self.print_options()
            self.select_option(input("Enter the number of the action you would like to perform: "))
            os.system('cls')
        
        if self._INFO_ALTERED:
            self.write_programs()
        
        self._temp_setup_exe_location.cleanup()


if __name__ == "__main__":
    manager = ProgramManager()
    manager.run()