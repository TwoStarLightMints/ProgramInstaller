from tempfile import TemporaryDirectory
import sqlite3
from program import Program

# sqlite3 database structure
#   Table: programs
#       Rows: (Program Name, Download Link)

class ProgramManager:
    def __init__(self):
        self._temp_dir = TemporaryDirectory()
        self.program_list: list[Program] = list()
    
    def get_progrms(self):
        pass

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

    def print_options(self):
        pass