from tempfile import TemporaryDirectory
import requests
import sqlite3
from program import Program

# sqlite3 database structure
#   Table: programs
#       Rows: (Program Name, Download Link)

class ProgramManager:
    def __init__(self):
        self._temp_dir = TemporaryDirectory()
        self.program_list: list[Program] = list()
    
    def get_programs(self):
        sql_con = sqlite3.connect("install_programs.db")
        sql_cur = sql_con.cursor()

        res = sql_cur.execute("SELECT * FROM programs")

        for row in res.fetchall():
            self.program_list.append(Program(row[1], row[2]))

    def write_programs(self):
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
        for program in self.program_list:
            print(program)
        
    def add_program(self):
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

if __name__ == "__main__":
    pass