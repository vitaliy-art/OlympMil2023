from abc import ABC, abstractmethod
from typing import List
from model.vehicle import Vehicle
from model.component import Component
from config.config import Config


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

    def get_vehicle_types(self) -> List[str]:
        """Get vehicle types"""

    def get_components(self) -> List[Component]:
        """Get components"""
