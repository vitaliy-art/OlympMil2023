import json
from typing import Dict, List

from config.config import Config
from model.component import Component
from model.vehicle import Vehicle
from storage.storage import Storage


class StorageJSON(Storage):
    """JSON storage implementation"""

    def _set_cfg(self, val: Config):
        self.cfg = val

    def _vehicles_file_name(self):
        return self.cfg.json_path + "vehicles.json"

    def _components_file_name(self):
        return self.cfg.json_path + "components.json"

    def _vehicle_to_dict(v: Vehicle):
        return {
            "code": v.code,
            "name": v.name,
            "type": v.type,
        }

    def _component_to_dict(c: Component):
        return {
            "code": c.code,
            "name": c.name,
            "price": c.price,
            "destroyed": c.destroyed,
            "vehicle": c.vehicle,
        }

    def save_vehicles(self, vehicles: List[Vehicle]):
        with open(self._vehicles_file_name, 'r+') as f:
            storedList: List[Vehicle] = json.load(
                f, object_hook=lambda x: self._vehicle_from_dict(x)
            )

            mappedVehicles: Dict[int, Vehicle] = {
                s.code: s for s in storedList
            }

            for v in vehicles:
                mappedVehicles[v.code] = v

            storedList = (
                self._vehicle_to_dict(v) for v in mappedVehicles.values()
            )

            json.dump(storedList, f)

    def save_components(self, components: List[Component]):
        with open(self._components_file_name, 'r+') as f:
            storedList: List[Component] = json.load(
                f, object_hook=lambda x: self._component_from_dict(x)
            )

            mappedComponents: Dict[int, Component] = {
                s.code: s for s in storedList
            }

            for c in components:
                mappedComponents[c.code] = c

            storedList = (
                self._component_to_dict(c) for c in mappedComponents.values()
            )

            json.dump(storedList, f)

    def get_vehicles(self) -> List[Vehicle]:
        vehicles: List[Vehicle] = []
        components: List[Component] = []
        with open(self._vehicles_file_name, 'r') as f:
            vehicles = json.load(
                f, object_hook=lambda x: self._vehicle_from_dict(x)
            )

        with open(self._components_file_name, 'r') as f:
            components = json.load(
                f, object_hook=lambda x: self._component_from_dict(x)
            )

        for v in vehicles:
            v.components = [
                c for c in components if c.vehicle == v.code
            ]

        return vehicles

    def get_vehicle_types(self) -> List[str]:
        with open(self._vehicles_file_name, 'r') as f:
            vehicles = json.load(
                f, object_hook=lambda x: self._vehicle_from_dict(x)
            )

            return list({
                v.type for v in vehicles
            })

    def get_components(self) -> List[Component]:
        with open(self._components_file_name, 'r') as f:
            return json.load(
                f, object_hook=lambda x: self._component_from_dict(x)
            )
