import json
from typing import List

from config.config import DB, Action, Config
from model.component import Component, ComponentEncoder
from model.vehicle import Vehicle, VehicleEncoder
from storage.storage import Storage
from storage.storage_json import StorageJSON
from storage.storage_sqlite import StorageSQLite


class Executor:

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.storage: Storage = self._get_storage(cfg)

    def _get_storage(self, cfg: Config) -> Storage:
        match cfg.db_type:
            case DB.FILE:
                return StorageJSON(cfg)
            case DB.SQLITE:
                return StorageSQLite(cfg)
            case _:
                raise TypeError(f"unexpected database type: {cfg.db_type}")

    def _save_vehicles(self):
        input_file = self.cfg.input_file
        vehicles: List[Vehicle] = []
        with open(input_file, 'r') as f:
            vehicles = json.load(
                f, object_hook=lambda x: Vehicle.from_dict(x)
            )

        self.storage.save_vehicles(vehicles)

    def _save_components(self):
        input_file = self.cfg.input_file
        components: List[Component] = []
        with open(input_file, 'r') as f:
            components = json.load(
                f, object_hook=lambda x: Component.from_dict(x)
            )

        self.storage.save_components(components)

    def _add_vehicles(self):
        self._save_vehicles()

    def _add_components(self):
        self._save_components()

    def _update_vehicles(self):
        self._save_vehicles()

    def _update_components(self):
        self._save_components()

    def _get_output_file(self):
        output_file = self.cfg.output_file
        if output_file == "":
            raise ValueError("output file not specified")

        return output_file

    def _get_vehicle_code(self):
        code = self.cfg.vehicle_code
        if code == "":
            raise ValueError("vehicle code not specified")

        return code

    def _show_all_vehicles(self):
        output_file = self._get_output_file()
        vehicles = self.storage.get_vehicles()
        with open(output_file, 'w') as f:
            json.dump(vehicles, f, cls=VehicleEncoder)

    def _show_all_components(self):
        output_file = self._get_output_file()
        components = self.storage.get_components()
        with open(output_file, 'w') as f:
            json.dump(components, f, cls=ComponentEncoder)

    def _show_vehicle_types(self):
        output_file = self._get_output_file()
        types = self.storage.get_vehicle_types()
        with open(output_file, 'w') as f:
            json.dump(types, f)

    def _show_destroyed_vehicles(self):
        output_file = self._get_output_file()
        vehicles = self.storage.get_vehicles()
        destroyed = [
            v for v in vehicles
            if len([c for c in v.components if c.destroyed]) /
            len(v.components) >= .6
        ]

        with open(output_file, 'w') as f:
            json.dump(destroyed, f, cls=VehicleEncoder)

    def _show_serviceable_vehicles(self):
        output_file = self._get_output_file()
        vehicles = self.storage.get_vehicles()
        serviceable = [
            v for v in vehicles
            if len([c for c in v.components if c.destroyed]) /
            len(v.components) < .6
        ]

        with open(output_file, 'w') as f:
            json.dump(serviceable, f, cls=VehicleEncoder)

    def _show_vehicle(self):
        output_file = self._get_output_file()
        code = self._get_vehicle_code()

        vehicles = self.storage.get_vehicles()
        text = ""
        for v in vehicles:
            if v.code == code:
                text = json.dumps(v, cls=VehicleEncoder)
                break

        with open(output_file, 'w') as f:
            f.write(text)

    def _show_destroyed_components(self):
        output_file = self._get_output_file()
        components = self.storage.get_components()
        destroyed = [
            c for c in components if c.destroyed
        ]

        with open(output_file, 'w') as f:
            json.dump(destroyed, f, cls=ComponentEncoder)

    def _show_destroyed_vehicle_components(self):
        output_file = self._get_output_file()
        code = self._get_vehicle_code()
        components = self.storage.get_components()
        destroyed = [
            c for c in components if c.vehicle == code and c.destroyed
        ]

        with open(output_file, 'w') as f:
            json.dump(destroyed, f, cls=ComponentEncoder)

    def _show_serviceable_components(self):
        output_file = self._get_output_file()
        components = self.storage.get_components()
        serviceable = [
            c for c in components if not c.destroyed
        ]

        with open(output_file, 'w') as f:
            json.dump(serviceable, f, cls=ComponentEncoder)

    def _show_serviceable_vehicle_components(self):
        output_file = self._get_output_file()
        code = self._get_vehicle_code()
        components = self.storage.get_components()
        serviceable = [
            c for c in components if c.vehicle == code and not c.destroyed
        ]

        with open(output_file, 'w') as f:
            json.dump(serviceable, f, cls=ComponentEncoder)

    def _show_vehicle_damage(self):
        output_file = self._get_output_file()
        code = self._get_vehicle_code()
        components = self.storage.get_components()
        vehicle_components = [
            c for c in components if c.vehicle == code
        ]

        damage = len([c for c in vehicle_components if c.destroyed]) \
            / len(vehicle_components)

        with open(output_file, 'w') as f:
            f.write(str(damage))

    def execute(self):
        match self.cfg.action:
            case Action.ADD_VEHICLES:
                self._add_vehicles()
            case Action.ADD_COMPONENTS:
                self._add_components()
            case Action.UPDATE_VEHICLES:
                self._update_vehicles()
            case Action.UPDATE_COMPONENTS:
                self._update_components()
            case Action.SHOW_ALL_VEHICLES:
                self._show_all_vehicles()
            case Action.SHOW_ALL_COMPONENTS:
                self._show_all_components()
            case Action.SHOW_VEHICLE_TYPES:
                self._show_vehicle_types()
            case Action.SHOW_DESTROYED_VEHICLES:
                self._show_destroyed_vehicles()
            case Action.SHOW_SERVICEABLE_VEHICLES:
                self._show_serviceable_vehicles()
            case Action.SHOW_VEHICLE:
                self._show_vehicle()
            case Action.SHOW_DESTROYED_COMPONENTS:
                self._show_destroyed_components()
            case Action.SHOW_DESTROYED_VEHICLE_COMPONENTS:
                self._show_destroyed_vehicle_components()
            case Action.SHOW_SERVICEABLE_COMPONENTS:
                self._show_serviceable_components()
            case Action.SHOW_SERVICEABLE_VEHICLE_COMPONENTS:
                self._show_serviceable_vehicle_components()
            case Action.SHOW_VEHICLE_DAMAGE:
                self._show_vehicle_damage()
            case _:
                raise TypeError(f"unexpected action type: {self.cfg.action}")
