from tempfile import TemporaryDirectory
from os import listdir
import requests
import sqlite3
from program import Program
from time import sleep

# sqlite3 database structure
#   Table: programs
#       Rows: (Program Name, Download Link)

class ProgramManager:
    def __init__(self):
        self._temp_dir = TemporaryDirectory()
        self.program_list: list[Program] = list()
    
    def get_programs(self):
        """
        Reads all programs currently stored in the local sqlite3 database and loads them into program list
        """
        sql_con = sqlite3.connect("install_programs.db")
        sql_cur = sql_con.cursor()

        res = sql_cur.execute("SELECT * FROM programs")

        for row in res.fetchall():
            self.program_list.append(Program(row[1], row[2]))

    def write_programs(self):
        """
        Writes all programs currently in the program list to the local sqlite3 database.
        """
        sql_con = sqlite3.connect("install_programs.db")
        sql_cur = sql_con.cursor()
        
        res = sql_cur.execute("SELECT name FROM sqlite_master")
        
        if res.fetchone() is None:
            sql_cur.execute("CREATE TABLE programs (program_name, download_link)")
        
        for program in self.program_list:
            res = sql_cur.execute(f"SELECT * FROM programs WHERE program_name='{program.program_name}'")

            if res.fetchone() == None:
                continue
            sql_cur.execute(f"INSERT INTO programs VALUES ({program.program_name}, {program.download_link})")
        
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
        link_ready = False
        link = ""

        while not link_ready:
            link = input("Please enter the download link for the program: ")
            
            print("\nTesting link...")
            if link != "":
                resp = requests.get(link)

                if resp.ok:
                    print("Download link is valid, now adding program...")
                    self.program_list.append(Program(link, prog_name, self._temp_dir.name))
                    link_ready = True
                else:
                    print("Download link responded with an error code, please check your spelling or enter a different link.")
    
    def download_setups(self):
        """
        Calls the install method of all programs in the program list to download their executables and then uses system to start the process.
        """
        print("Retrieving exectuables for programs...")
        
        for program in self.program_list:
            program.install()

if __name__ == "__main__":
    pass