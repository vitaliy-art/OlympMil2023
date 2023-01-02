from enum import Enum
import sys


_use_file = "-file"
_use_sqlite = "-sqlite"
_use_postgres = "-postgres"
_read_from_file = "--input="
_write_to_file = "--output="


class Config:
    def __init__(self):
        self.args = sys.argv[1:]
        self.db = DB.UNKNOWN
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
            elif arg == _use_postgres:
                self.db = DB.POSTGRES
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
    POSTGRES = 3
