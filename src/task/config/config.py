from enum import Enum
import sys
import os


_use_file = "-file"
_use_sqlite = "-sqlite"
_db_file_name = "--db_name="
_read_from_file = "--input="
_write_to_file = "--output="


class Config:
    def __init__(self):
        self.args = sys.argv[1:]
        self.db = DB.UNKNOWN
        self.db_file_name = "database"
        self.json_path = "." + os.sep
        self.input_file = ""
        self.output_file = ""

    def _parse_write_to(self):
        for arg in self.args:
            if arg == _use_file:
                self.db = DB.FILE
                break
            elif arg == _use_sqlite:
                self.db = DB.SQLITE
                break

    def _parse_db_name(self):
        for arg in self.args:
            if arg == _db_file_name:
                self.db_file_name = arg.replace(_db_file_name, "", 1)
                break

    def _parse_input_file(self):
        for arg in self.args:
            if arg.startswith(_read_from_file):
                self.input_file = arg.replace(_read_from_file, "", 1)
                break

    def _parse_output_file(self):
        for arg in self.args:
            if arg.startswith(_write_to_file):
                self.output_file = arg.replace(_write_to_file, "", 1)
                break

    def parse_args(self):
        self._parse_write_to()
        self._parse_input_file()


class DB(Enum):
    UNKNOWN = 0
    FILE = 1
    SQLITE = 2
