import json
from typing import Dict, List

from config.config import Config
from model.component import Component, ComponentEncoder
from model.vehicle import Vehicle, VehicleEncoder
from storage.storage import Storage


class StorageJSON(Storage):
    """JSON storage implementation"""

    def __init__(self, cfg: Config):
        super().__init__(cfg)

    def _vehicles_file_name(self):
        return self.cfg.json_path + "vehicles.json"

    def _components_file_name(self):
        return self.cfg.json_path + "components.json"

    def save_vehicles(self, vehicles: List[Vehicle]):
        with open(self._vehicles_file_name, 'r+') as f:
            storedList = json.load(
                f, object_hook=lambda x: Vehicle.from_dict(x)
            )  # type: List[Vehicle]

            mappedVehicles = {
                s.code: s for s in storedList
            }  # type: Dict[int, Vehicle]

            for v in vehicles:
                mappedVehicles[v.code] = v

            storedList = [
                v.to_dict() for v in mappedVehicles.values()
            ]

            json.dump(storedList, f, cls=VehicleEncoder)

    def save_components(self, components: List[Component]):
        with open(self._components_file_name, 'r+') as f:
            storedList = json.load(
                f, object_hook=lambda x: Component.from_dict(x)
            )  # type: List[Component]

            mappedComponents = {
                s.code: s for s in storedList
            }  # type: Dict[int, Component]

            for c in components:
                mappedComponents[c.code] = c

            storedList = [
                c.to_dict() for c in mappedComponents.values()
            ]

            json.dump(storedList, f, cls=ComponentEncoder)

    def get_vehicles(self) -> List[Vehicle]:
        vehicles = []  # type: List[Vehicle]
        components = []  # type: List[Component]
        with open(self._vehicles_file_name, 'r') as f:
            vehicles = json.load(
                f, object_hook=lambda x: Vehicle.from_dict(x)
            )

        with open(self._components_file_name, 'r') as f:
            components = json.load(
                f, object_hook=lambda x: Component.from_dict(x)
            )

        for v in vehicles:
            v.components = [
                c for c in components if c.vehicle == v.code
            ]

        return vehicles

    def get_vehicle_types(self) -> List[str]:
        with open(self._vehicles_file_name, 'r') as f:
            vehicles = json.load(
                f, object_hook=lambda x: Vehicle.from_dict(x)
            )

            return list({
                v.type for v in vehicles
            })

    def get_components(self) -> List[Component]:
        with open(self._components_file_name, 'r') as f:
            return json.load(
                f, object_hook=lambda x: Component.from_dict(x)
            )
