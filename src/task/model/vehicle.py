import json
from typing import Dict, List, Any

from model.component import Component


class Vehicle:
    """Vehicle"""

    def __init__(self):
        self.code = ""
        self.name = ""
        self.type = ""
        self.components = []  # type: List[Component]

    @staticmethod
    def from_dict(d: Dict[str, any]):
        vehicle = Vehicle()
        vehicle.code = d["code"]
        vehicle.name = d["name"]
        vehicle.type = d["type"]
        return vehicle

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "type": self.type,
        }

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        if self.code != __o.code:
            return False

        if self.name != __o.name:
            return False

        if self.type != __o.type:
            return False

        return True


class VehicleEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Vehicle):
            return o.__dict__
        elif isinstance(o, Component):
            return o.__dict__

        return json.JSONEncoder.default(self, o)
