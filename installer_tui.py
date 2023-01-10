from program_manager import ProgramManager
from os import system, listdir, chdir, getcwd
from time import sleep

class TUI_Mngr:
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
    
    def install_programs(self):
        self.manager.download_setups()

        cwd = getcwd()

        q = input("Continue with install? (y/n) ")

        if q == "y":
            chdir(self.manager._temp_dir.name)

            for setup in listdir():
                system(setup)
            
            chdir(cwd)
    
    def run(self):
        running = True

        while running:
            self.print_menu()
            choice = self.get_option("Enter your choice: ", "int")
            if choice == 0:
                running = False
                continue
            self.method_dict(choice)

        print("Cleaning up...")
        self.manager._temp_dir.cleanup()

if __name__ == "__main__":
    tui = TUI_Mngr()