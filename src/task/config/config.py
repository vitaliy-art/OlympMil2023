import os
import sys
from enum import Enum

_use_file = "-file"
_use_sqlite = "-sqlite"

_json_path = "--json_path="
_db_file_name = "--db_name="

_add_vehicles = "--add_vehicles"
_add_components = "--add_components"
_update_vehicles = "--update_vehicles"
_update_components = "--update_components"

_all_vehicles = "--all_vehicles"
_all_components = "--all_components"
_vehicle_types = "--vehicle_types"
_destroyed_vehicles = "--destroyed_vehicles"
_serviceable_vehicles = "--serviceable_vehicles"

_destroyed_components = "--destroyed_components"
_serviceable_components = "--serviceable_components"
_vehicle_damage = "--vehicle_damage"

_vehicle_code = "--vehicle_code="

_read_from_file = "--input="
_write_to_file = "--output="


class Config:
    def __init__(self):
        self.args = sys.argv[1:]
        self.db = DB.UNKNOWN
        self.db_file_name = "database"
        self.json_path = "." + os.sep
        self.db_file_name = "bd.db"
        self.input_file = ""
        self.output_file = ""
        self.action = Action.UNKNOWN
        self.vehicle_code = ""

    def _parse_write_to(self):
        for arg in self.args:
            if arg == _use_file:
                self.db = DB.FILE
                break
            elif arg == _use_sqlite:
                self.db = DB.SQLITE
                break

    def _parse_json_path(self):
        for arg in self.args:
            if arg == _json_path:
                self.json_path = arg.replace(_json_path, "", 1)
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

    def _parse_action(self):
        for arg in self.args:
            if arg == _add_vehicles:
                self.action = Action.ADD_VEHICLES
                break
            elif arg == _add_components:
                self.action = Action.ADD_COMPONENTS
                break
            elif arg == _update_vehicles:
                self.action = Action.UPDATE_VEHICLES
                break
            elif arg == _update_components:
                self.action = Action.UPDATE_COMPONENTS
                break
            elif arg == _all_vehicles:
                self.action = Action.SHOW_ALL_VEHICLES
                break
            elif arg == _all_components:
                self.action = Action.SHOW_ALL_COMPONENTS
                break
            elif arg == _vehicle_types:
                self.action = Action.SHOW_VEHICLE_TYPES
                break
            elif arg == _destroyed_vehicles:
                self.action = Action.SHOW_DESTROYED_VEHICLES
                break
            elif arg == _serviceable_vehicles:
                self.action = Action.SHOW_SERVICEABLE_VEHICLES
                break
            elif arg == _destroyed_components:
                self.action = Action.SHOW_DESTROYED_COMPONENTS
                break
            elif arg == _serviceable_components:
                self.action = Action.SHOW_SERVICEABLE_COMPONENTS
                break
            elif arg == _vehicle_damage:
                self.action = Action.SHOW_VEHICLE_DAMAGE
                break

    def _parse_vehicle_code(self):
        for arg in self.args:
            if arg.startswith(_vehicle_code):
                self.vehicle_code = arg.replace(_vehicle_code, "", 1)
                break

    def parse_args(self):
        self._parse_write_to()
        self._parse_json_path()
        self._parse_db_name()
        self._parse_input_file()
        self._parse_output_file()
        self._parse_action()
        self._parse_vehicle_code()


class DB(Enum):
    UNKNOWN = 0
    FILE = 1
    SQLITE = 2


class Action(Enum):
    UNKNOWN = 0
    ADD_VEHICLES = 1
    ADD_COMPONENTS = 2
    UPDATE_VEHICLES = 3
    UPDATE_COMPONENTS = 4
    SHOW_ALL_VEHICLES = 5
    SHOW_ALL_COMPONENTS = 6
    SHOW_VEHICLE_TYPES = 7
    SHOW_DESTROYED_VEHICLES = 8
    SHOW_SERVICEABLE_VEHICLES = 9
    SHOW_VEHICLE = 10
    SHOW_DESTROYED_COMPONENTS = 11
    SHOW_DESTROYED_VEHICLE_COMPONENTS = 12
    SHOW_SERVICEABLE_COMPONENTS = 13
    SHOW_SERVICEABLE_VEHICLE_COMPONENTS = 14
    SHOW_VEHICLE_DAMAGE = 15
