import sqlite3
from typing import List, Any

from config.config import Config
from model.component import Component
from model.vehicle import Vehicle
from storage.storage import Storage

_INIT_SQL = """
    CREATE TABLE IF NOT EXISTS vehicles (
        code TEXT PRIMARY KEY,
        name TEXT,
        type TEXT
    );

    CREATE TABLE IF NOT EXISTS components (
        code TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        destroyed INTEGER NOT NULL CHECK (destroyed IN (0, 1)),
        vehicle TEXT,

        FOREIGN KEY(vehicle) REFERENCES vehicles(code)
    );
"""

_ALL_VEHICLES_SQL = "SELECT * FROM vehicles;"
_ALL_COMPONENTS_SQL = "SELECT * FROM components;"

_INSERT_VEHICLE_SQL = """
    INSERT INTO vehicles (code, name, type) VALUES (?, ?, ?);
"""

_INSERT_COMPONENT_SQL = """
    INSERT INTO components (code, name, price, destroyed, vehicle)
    VALUES (?, ?, ?, ?, ?);
"""

_UPDATE_VEHICLE_SQL = "UPDATE vehicles SET name = ?, type = ? WHERE code = ?;"
_UPDATE_COMPONENT_SQL = """
    UPDATE components SET name = ?, price = ?, destroyed = ?, vehicle = ?
    WHERE code = ?;
"""


class StorageSQLite(Storage):
    """SQLite3 storage implementation"""

    def __init__(self, cfg: Config):
        super().__init__(cfg)

    def _db_file_name(self):
        return self.cfg.db_file_name

    def _get_connection(self):
        cx = sqlite3.connect(self._db_file_name())
        cx.executescript(f"PRAGMA foreign_keys = ON;{_INIT_SQL}")
        cx.row_factory = self._dict_factory
        return cx

    def _dict_factory(self, cursor: sqlite3.Cursor, row: List[Any]):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]

        return d

    def save_vehicles(self, vehicles: List[Vehicle]):
        with self._get_connection() as cx:
            cu = cx.cursor()
            storedVehicles: List[Vehicle] = {
                r["code"]: Vehicle.from_dict(r)
                for r in cu.execute(_ALL_VEHICLES_SQL)
            }

            inserts: List[Vehicle] = []
            updates: List[Vehicle] = []
            for v in vehicles:
                if v.code not in storedVehicles:
                    inserts.append(v)
                    continue

                if storedVehicles[v.code] != v:
                    updates.append(v)

            for v in inserts:
                cu.execute(_INSERT_VEHICLE_SQL, (v.code, v.name, v.type,))

            for v in updates:
                cu.execute(_UPDATE_VEHICLE_SQL, (v.name, v.type, v.code,))

    def save_components(self, components: List[Component]):
        with self._get_connection() as cx:
            cu = cx.cursor()
            storedComponents: List[Component] = {
                r["code"]: Component.from_dict(r)
                for r in cu.execute(_ALL_COMPONENTS_SQL)
            }

            inserts: List[Component] = []
            updates: List[Component] = []
            for c in components:
                if c.code not in storedComponents:
                    inserts.append(c)
                    continue

                if storedComponents[c.code] != c:
                    updates.append(c)

            for c in inserts:
                cu.execute(
                    _INSERT_COMPONENT_SQL,
                    (c.code, c.name, c.price, c.destroyed, c.vehicle,),
                )

            for c in updates:
                cu.execute(
                    _UPDATE_COMPONENT_SQL,
                    (c.name, c.price, c.destroyed, c.vehicle, c.code,),
                )

    def get_vehicles(self) -> List[Vehicle]:
        with self._get_connection() as cx:
            cu = cx.cursor()
            vehicles: List[Vehicle] = [
                Vehicle.from_dict(r)
                for r in cu.execute(_ALL_VEHICLES_SQL)
            ]

            components: List[Component] = [
                Component.from_dict(r)
                for r in cu.execute(_ALL_COMPONENTS_SQL)
            ]

            for v in vehicles:
                v.components = [
                    c for c in components if c.vehicle == v.code
                ]

            return vehicles

    def get_vehicle_types(self) -> List[str]:
        with self._get_connection() as cx:
            cu = cx.cursor()
            vehicles: List[Vehicle] = (
                Vehicle.from_dict(r)
                for r in cu.execute(_ALL_VEHICLES_SQL)
            )

            return list({
                v.type for v in vehicles
            })

    def get_components(self) -> List[Component]:
        with self._get_connection() as cx:
            cu = cx.cursor()
            return [
                Component.from_dict(r)
                for r in cu.execute(_ALL_COMPONENTS_SQL)
            ]
