from typing import List
from model.component import Component


class Vehicle:
    """Vehicle"""

    def __init__(self):
        self.code = ""
        self.name = ""
        self.type = ""
        self.components = []  # type: List[Component]

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
