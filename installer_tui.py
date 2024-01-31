import os
from program_manager import ProgramManager
from os import listdir, chdir, getcwd
from subprocess import run as run_sb
from os import system

class TUI_Mngr:
    def __init__(self) -> None:
        # Used to track if the list of programs has been altered in any way
        self._state_change = False
        self.manager = ProgramManager()
        # When an instance of TUI_Mngr has been instantiated, run the tui
        self.run()

    def clear_screen(self):
        # This method is abstracted out due to provide the avility to support multiple OSs
        system("clear")
        
    def print_menu(self):
        print("-- PROGRAM INSTALLER --")
        print("\nMain Menu\n")
        print("\t1. Help")
        print("\t2. View list of programs")
        print("\t3. Add a program")
        print("\t4. Install all programs")
        print("\t5. Edit a program")
        print("\t6. Remove a program")
        print("\t7. Update the link information for all programs")
        print("\t9. Save changes")
        print("\t0. Quit")
        print("\n")

    def continue_q_mark(self):
        # Abstracted away because it is used often
        input("Please enter to continue...")
    
    def get_option_num(self, prompt: str) -> int:
        # Used as an abstraction to safely get an option from the user
        resp = input(prompt)

        try:
            return int(resp)
        except ValueError:
            print("Invalid input, please enter an integer.")
            return self.get_option_num(prompt)
    
    def method_dict(self, choice: int):
        # Maps integers to methods
        methods = {
            1: self.this_help,
            2: self.show_programs,
            3: self.add_program,
            4: self.install_programs,
            5: self.edit_program,
            6: self.remove_program,
            7: self.update_link_info,
            9: self.save_changes,
        }

        method = methods.get(choice)

        if method is None:
            print("Invalid selection, please enter a valid option.")
            return

        method()

    def this_help(self):
        # This is the help that will be displayed when the user selects the help option
        print("Program Installer")
        print("\nThis program is a TUI which allows you to create a list of programs including their download links for you to be able to easily install those programs all at once.")
        print("\nTo run the script just use:")
        print("\n\t$ python main.py")
        print("\nMore to come.")
        self.continue_q_mark()
    
    def show_programs(self):
        self.manager.show_programs()
        self.continue_q_mark()
    
    def add_program(self):
        self.manager.add_program()
        self._state_change = True

    def edit_program(self):
        self.manager.show_programs()
        print("")
        program_num = self.get_option_num("Enter the number of the program you would like to edit: ") - 1
        field = self.get_option_num("Enter the field which you would like to edit (1: Program Name 2: Download Link): ")

        new_val = None
        choice_good = False

        while not choice_good:
            if field == 1:
                new_val = input("Please enter the new name for the program: ")
                choice_good = True

            elif field == 2:
                new_val = input("Please enter the new download link for the program: ")
                choice_good = True
            
            else:
                print(f"Please enter either '1' or '2'.")

        if not new_val is None:
            self.manager.edit_program(program_num, field, new_val)

    def update_link_info(self):
        if 'y' == input("This process can take a while to complete, continue? (y/n) "):
            self._state_change = True
            self.manager.update_link_info()
    
    def install_programs(self):
        self.manager.download_setups()

        if "y" == input("Continue with install? (y/n) "):
            for program in self.manager.program_list:
                print(program.temp_path)

                try:
                    run_sb(program.temp_path)

                except OSError:
                    print(f"Something went wrong installing {program.program_name}, try using a different download link.\nIf you can find a link that has any kind of version information or has the display text: 'Download should start in a few seconds, -if not click here-'.")
                self.continue_q_mark()
    
    def save_changes(self):
        if "y" == input("Save changes? (y/n) "):
            if self._state_change:
                self.manager.write_programs()
                self._state_change = False
            else:
                print("No changes to save")
                self.continue_q_mark()
    
    def remove_program(self):
        self.manager.show_programs()
        print("")

        choice_made = False
        choice = None
        prog_num = -1
        
        while not choice_made:
            prog_num = self.get_option_num("Enter the number of the program you would like to remove: ") - 1
            if prog_num < 0 or prog_num > len(self.manager.program_list):
                print(f"Please enter a number greater than zero and less than {len(self.manager.program_list)}")
                continue
            elif str(prog_num).lower() == 'c':
                print("Program deletion aborted")
                self.continue_q_mark()
                return
            else:
                choice_made = True
                choice = input(f"Are you sure you want to delete {self.manager.program_list[prog_num].program_name}? (y/n) ")

        if choice == 'y' and not choice is None and prog_num != -1:
            self.manager.remove_program(prog_num)
            self._state_change = True
    
    def run(self):
        running = True

        self.clear_screen()
        
        while running:
            self.print_menu()
            choice = self.get_option_num("Enter your choice: ")
            if choice == 0:
                running = False
                continue
            self.clear_screen()
            self.method_dict(choice)
            self.clear_screen()
        
        if self._state_change:
            self.save_changes()

        print("Cleaning up...")
        self.manager._temp_dir.cleanup()
        self.manager.db_con.close()

if __name__ == "__main__":
    pass
