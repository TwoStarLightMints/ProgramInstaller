from program_manager import ProgramManager
from os import system, listdir, chdir, getcwd
from time import sleep
import subprocess as sp

class TUI_Mngr:
    _STATE_CHANGE_ = False
    def __init__(self) -> None:
        self.manager = ProgramManager()
        self.run()

    def print_menu(self):
        print("-- PROGRAM INSTALLER --")
        print("\nMain Menu\n")
        print("\t1. Help")
        print("\t2. View list of programs")
        print("\t3. Add a program")
        print("\t4. Install all programs")
        print("\t9. Save changes")
        print("\t0. Quit")
        print("\n")
    
    def get_option(self, prompt: str, type: str):
        resp = input(prompt)

        if type == "int":
            try:
                return int(resp)
            except ValueError:
                print("Invalid input, please enter an integer.")
                return self.get_option(prompt, type)
        return resp
    
    def method_dict(self, choice: int):
        methods = {
            1: self.this_help,
            2: self.show_programs,
            3: self.add_program,
            4: self.install_programs,
            9: self.save_changes,
        }

        try:
            methods.get(choice)()
        except TypeError:
            print("Invalid selection, please enter a valid option.")

    def this_help(self):
        print("Program Installer")
        print("\nThis program is a TUI which allows you to create a list of programs including their download links for you to be able to easily install those programs all at once.")
        print("\nTo run the script just use:")
        print("\n\t$ python main.py")
        print("\nMore to come.")
    
    def show_programs(self):
        self.manager.show_programs()
    
    def add_program(self):
        self.manager.add_program()
        self._STATE_CHANGE_ = True
    
    def install_programs(self):
        self.manager.download_setups()

        cwd = getcwd()

        q = input("Continue with install? (y/n) ")

        if q == "y":
            chdir(self.manager._temp_dir.name)

            for setup in listdir():
                sp.run(setup)
            
            chdir(cwd)
    
    def save_changes(self):
        q = input("Save changes? (y/n) ")

        if q == "y":
            if self._STATE_CHANGE_:
                self.manager.write_programs()
                self._STATE_CHANGE_ = False
            else:
                print("No changes to save")
    
    def run(self):
        running = True

        while running:
            self.print_menu()
            choice = self.get_option("Enter your choice: ", "int")
            if choice == 0:
                running = False
                continue
            self.method_dict(choice)
        
        if self._STATE_CHANGE_:
            self.save_changes()

        print("Cleaning up...")
        self.manager._temp_dir.cleanup()
        self.manager.db_con.close()

if __name__ == "__main__":
    pass