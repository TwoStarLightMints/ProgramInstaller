from tempfile import TemporaryDirectory
from os import listdir
from os.path import isfile
import requests
import sqlite3
from program import Program
from time import sleep

# sqlite3 database structure
#   Table: programs
#       Rows: (Program Name, Download Link)

class ProgramManager:
    _DATABASE_ = "install_programs.db"

    def __init__(self):
        self._temp_dir = TemporaryDirectory()
        self.program_list: list[Program] = list()

        self.get_programs()
    
    def get_programs(self):
        """
        Reads all programs currently stored in the local sqlite3 database and loads them into program list
        """
        if isfile(self._DATABASE_):
            sql_con = sqlite3.connect(self._DATABASE_)
            sql_cur = sql_con.cursor()

            res = sql_cur.execute("SELECT * FROM programs")

            for row in res.fetchall():
                self.program_list.append(Program(row[1], row[0], self._temp_dir.name))

            sql_con.close()
        else:
            sql_con = sqlite3.connect(self._DATABASE_)
            sql_cur = sql_con.cursor()
            
            sql_cur.execute("CREATE TABLE programs (program_name, download_link)")

            sql_con.close()

    def write_programs(self):
        """
        Writes all programs currently in the program list to the local sqlite3 database.
        """
        sql_con = sqlite3.connect("install_programs.db")
        sql_cur = sql_con.cursor()
        
        for program in self.program_list:
            res = sql_cur.execute(f"SELECT * FROM programs WHERE program_name='{program.program_name}'")

            if res.fetchone() == None:
                print(f"Writing - {program}")
                sql_cur.execute(f"INSERT INTO programs VALUES ('{program.program_name}', '{program.download_link}')")
            else:
                continue
        
        sql_con.commit()
    
    def show_programs(self):
        """
        Prints out all the programs in the program list using their to string method.
        """
        for program in self.program_list:
            print(program)
        
    def add_program(self):
        """
        Exposes functionality to add a program to the list of programs.
        """
        prog_name = input("Please input a name for the program: ")
        link = input(f"Please enter the download link for {prog_name}: ")
        self.program_list.append(Program(link, prog_name, self._temp_dir.name))
    
    def download_setups(self):
        """
        Calls the install method of all programs in the program list to download their executables and then uses system to start the process.
        """
        print("Retrieving exectuables for programs...")
        
        for program in self.program_list:
            program.install()

if __name__ == "__main__":
    pass