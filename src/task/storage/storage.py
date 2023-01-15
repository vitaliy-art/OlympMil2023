from abc import ABC, abstractmethod
from typing import Dict, List

from config.config import Config
from model.component import Component
from model.vehicle import Vehicle


class Storage(ABC):

    def _get_cfg(self) -> Config:
        return self.cfg

    @abstractmethod
    def _set_cfg(self, val: Config):
        """Save configuration"""

    cfg = property(_get_cfg, _set_cfg)

    @abstractmethod
    def save_vehicles(self, vehicles: List[Vehicle]):
        """Save vehicles"""

    @abstractmethod
    def save_components(self, components: List[Component]):
        """Save components"""

    @abstractmethod
    def get_vehicles(self) -> List[Vehicle]:
        """Get vehicles"""

    @abstractmethod
    def get_vehicle_types(self) -> List[str]:
        """Get vehicle types"""

    @abstractmethod
    def get_components(self) -> List[Component]:
        """Get components"""

    def _vehicle_from_dict(d: Dict[str, any]):
        vehicle = Vehicle()
        vehicle.code = d["code"]
        vehicle.name = d["name"]
        vehicle.type = d["type"]
        return vehicle

    def _component_from_dict(d: Dict[str, any]):
        component = Component()
        component.code = d["code"]
        component.name = d["name"]
        component.price = d["price"]
        component.destroyed = bool(d["destroyed"])
        component.vehicle = d["vehicle"]
        return component
