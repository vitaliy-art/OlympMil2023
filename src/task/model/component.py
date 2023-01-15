from typing import Dict


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
