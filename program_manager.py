from tempfile import TemporaryDirectory
from os.path import isfile
import sqlite3
from program import Program
from linkfinder import LinkFinder
from time import sleep

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

            caught = res.fetchone()

            if caught == None:
                print(f"Writing - {program}")
                sql_cur.execute(f"INSERT INTO programs VALUES ('{id}', '{program.program_name}', '{program.download_link}')")
            elif caught != None:
                print(f"Updating {program.program_name}")
                sql_cur.execute(f"UPDATE programs SET program_name = '{program.program_name}', download_link = '{program.download_link}' WHERE id = '{id}'")
        
        self.db_con.commit()
    
    def show_programs(self):
        """
        Prints out all the programs in the program list using their to string method.
        """
        print("(Program Name): (Program Download Link)")
        print("")
        for num, program in enumerate(self.program_list):
            print(f"{num + 1}. {program}")
        
    def add_program(self, prog_name, link):
        """
        Exposes functionality to add a program to the list of programs.
        """
        self.program_list.append(Program(link, prog_name, self._temp_dir.name))

    def edit_program(self, program_num, field, new_val):
        if field == 1:
            self.program_list[program_num].program_name = new_val
        else:
            self.program_list[program_num].download_link = new_val

    def remove_program(self, program_num):
        sql_cur = self.db_con.cursor()
        sql_cur.execute(f"DELETE FROM programs WHERE program_name = '{self.program_list[program_num].program_name}'")
        self.program_list.remove(self.program_list[program_num])

    def update_link_info(self):
        for program in self.program_list:
            print(f"Now cleaning {program.program_name}, current link is {program.download_link}")
            old_link = program.download_link
            cleaner = LinkFinder(program.download_link)
            new_link = cleaner.clean_link
            print(f"New link for {program.program_name} is {new_link}")
            program.download_link = new_link
            
            if old_link != new_link:
                print(f"Consider updating your current version of {program.program_name}, the link was out of date")
    
    def download_setups(self):
        """
        Calls the install method of all programs in the program list to download their executables and then uses system to start the process.
        """
        print("Retrieving exectuables for programs...")
        
        for program in self.program_list:
            program.install()

if __name__ == "__main__":
    pass