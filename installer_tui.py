from program_manager import ProgramManager
from os import system

class TUI_Mngr:
    def __init__(self) -> None:
        self.method_dict(self.get_option("Just enter 1: ", "int"))

    def print_menu(self):
        print("-- PROGRAM INSTALLER --")
        print("Main Menu")
        print("1. Help")
        print("")
    
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
        }

        methods.get(choice)()

    def this_help(self):
        print("Program Installer")
        print("\nThis program is a TUI which allows you to create a list of programs including their download links for you to be able to easily install those programs all at once.")
        print("\nTo run the script just use:")
        print("\n\t$ python main.py")
        print("\nMore to come.")

if __name__ == "__main__":
    tui = TUI_Mngr()