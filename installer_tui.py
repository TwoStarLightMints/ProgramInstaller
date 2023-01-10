from program_manager import ProgramManager

class TUI_Mngr:
    def __init__(self) -> None:
        self.help()

    def help(self):
        print("Program Installer")
        print("\nThis program is a TUI which allows you to create a list of programs including their download links for you to be able to easily install those programs all at once.")

if __name__ == "__main__":
    tui = TUI_Mngr()