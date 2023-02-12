from program_manager import ProgramManager
from os import listdir, chdir, getcwd
from subprocess import run as run_sb
from os import system

class TUI_Mngr:
    def __init__(self) -> None:
        self._state_change = False
        self.manager = ProgramManager()
        self.run()

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
        input("Please enter to continue...")
    
    def get_option(self, prompt: str, type: str):
        resp = input(prompt)

        if type == "int":
            try:
                return int(resp)
            except ValueError:
                print("Invalid input, please enter an integer.")
                return self.get_option(prompt, type)
        return resp
    
    def check_is_in_range(self, lower, upper, choice):
        return (choice > lower and choice < upper)
    
    def method_dict(self, choice: int):
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
        self.continue_q_mark()
    
    def show_programs(self):
        self.manager.show_programs()
        self.continue_q_mark()
    
    def add_program(self):
        self.manager.add_program()
        self._state_change = True

    def edit_program(self):
        self.show_programs()
        program_num = self.get_option("Enter the number of the program you would like to edit: ", "int") - 1
        field = self.get_option("Enter the field which you would like to edit (1: Program Name 2: Download Link): ", "int")

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
        self.show_programs()

        choice_made = False
        
        while not choice_made:
            prog_num = self.get_option("Enter the number of the program you would like to remove: ", "int") - 1
            if prog_num < 0 or prog_num > len(self.manager.program_list):
                print(f"Please enter a number greater than zero and less than {len(self.manager.program_list)}")
                continue
            else:
                choice_made = "y" == input(f"Are you sure you want to delete {self.manager.program_list[prog_num].program_name}? (y/n) ")
        
        self.manager.remove_program(prog_num)
    
    def run(self):
        running = True

        system("cls")
        
        while running:
            self.print_menu()
            choice = self.get_option("Enter your choice: ", "int")
            if choice == 0:
                running = False
                continue
            system("cls")
            self.method_dict(choice)
            system("cls")
        
        if self._state_change:
            self.save_changes()

        print("Cleaning up...")
        self.manager._temp_dir.cleanup()
        self.manager.db_con.close()

if __name__ == "__main__":
    pass