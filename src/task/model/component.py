import json
from typing import Any, Dict


class Component:
    """Component"""

    def __init__(self):
        self.code = ""
        self.name = ""
        self.price = .0
        self.destroyed = False
        self.vehicle = ""

    @staticmethod
    def from_dict(d: Dict[str, any]):
        component = Component()
        component.code = d["code"]
        component.name = d["name"]
        component.price = d["price"]
        component.destroyed = bool(d["destroyed"])
        component.vehicle = d["vehicle"]
        return component

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "destroyed": self.destroyed,
            "vehicle": self.vehicle,
        }

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        if self.code != __o.code:
            return False

        if self.name != __o.name:
            return False

        if self.price != __o.price:
            return False

        if self.destroyed != __o.destroyed:
            return False

        if self.vehicle != __o.vehicle:
            return False

        return True


class ComponentEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Component):
            return o.__dict__

        return json.JSONEncoder.default(self, o)
