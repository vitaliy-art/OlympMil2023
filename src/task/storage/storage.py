from abc import ABC, abstractmethod
from typing import List

from config.config import Config
from model.component import Component
from model.vehicle import Vehicle


class Storage(ABC):

    def __init__(self, cfg: Config):
        self.cfg = cfg

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
