from tempfile import TemporaryDirectory
from os.path import isfile
import sqlite3
from program import Program
from linkfinder import LinkFinder

# sqlite3 database structure
#   Table: programs
#       Rows: (Program Name, Download Link)

class ProgramManager:
    _DATABASE_ = "install_programs.db"

    def __init__(self):
        self.db_con = self.retrieve_connection(self._DATABASE_)
        self._temp_dir = TemporaryDirectory()
        self.program_list: list[Program] = list()

        self.get_programs()
    
    def retrieve_connection(self, db_file):
        if isfile(db_file):
            return sqlite3.connect(db_file)
        else:
            sql_con = sqlite3.connect(db_file)
            sql_cur = sql_con.cursor()
            
            sql_cur.execute("CREATE TABLE programs (id PRIMARY KEY, program_name, download_link)")

            return sql_con
    
    def get_programs(self):
        """
        Reads all programs currently stored in the local sqlite3 database and loads them into program list
        """
        sql_cur = self.db_con.cursor()

        res = sql_cur.execute("SELECT * FROM programs")

        for row in res.fetchall():
            self.program_list.insert(int(row[0]), Program(row[2], row[1], self._temp_dir.name))

    def write_programs(self):
        """
        Writes all programs currently in the program list to the local sqlite3 database.
        """
        sql_cur = self.db_con.cursor()
        
        for id, program in enumerate(self.program_list):
            res = sql_cur.execute(f"SELECT * FROM programs WHERE id = '{id}'")

            if res.fetchone() == None:
                print(f"Writing - {program}")
                sql_cur.execute(f"INSERT INTO programs VALUES ('{id}', '{program.program_name}', '{program.download_link}')")
            elif res.fetchone() != None:
                sql_cur.execute(f"UPDATE programs SET program_name = '{program.program_name}', download_link = '{program.download_link}' WHERE id = '{id}'")
        
        self.db_con.commit()
    
    def show_programs(self):
        """
        Prints out all the programs in the program list using their to string method.
        """
        print("(Program Name): (Program Download Link)")
        for program in self.program_list:
            print(program)
        
    def add_program(self):
        """
        Exposes functionality to add a program to the list of programs.
        """
        prog_name = input("Please input a name for the program: ")
        link = input(f"Please enter the download link for {prog_name}: ")
        self.program_list.append(Program(link, prog_name, self._temp_dir.name))

    def edit_program(self, program_num, field, new_val):
        sql_cur = self.db_con.cursor()
        if field == 1:
            sql_cur.execute(f"UPDATE programs SET program_name = '{new_val}' WHERE id = '{program_num}'")
            self.program_list[program_num].program_name = new_val
        else:
            sql_cur.execute(f"UPDATE programs SET download_link = '{new_val}' WHERE id = '{program_num}'")
            self.program_list[program_num].download_link = new_val

    def remove_program(self, program_num):
        sql_cur = self.db_con.cursor()
        sql_cur.execute(f"DELETE FROM programs WHERE program_name = '{self.program_list[program_num].program_name}'")
        self.program_list.remove(self.program_list[program_num])

    def update_link_info(self):
        for id, program in enumerate(self.program_list):
            print(f"Now cleaning {program.program_name}")
            cleaner = LinkFinder(program.download_link)
            new_link = cleaner.clean_link
            print(f"New link for {program.program_name} is {new_link[:60]}")
            program.download_link = new_link
            sql_cur = self.db_con.cursor()
            sql_cur.execute(f"UPDATE programs SET download_link = '{new_link}' WHERE id = '{id}'")
    
    def download_setups(self):
        """
        Calls the install method of all programs in the program list to download their executables and then uses system to start the process.
        """
        print("Retrieving exectuables for programs...")
        
        for program in self.program_list:
            program.install()

if __name__ == "__main__":
    pass