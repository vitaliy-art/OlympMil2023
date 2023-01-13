from typing import List
from model.component import Component


class Vehicle:
    """Vehicle"""

    def __init__(self):
        self.code = ""
        self.name = ""
        self.type = ""
        self.components = []  # type: List[Component]
