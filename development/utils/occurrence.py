import os
from typing import Tuple, Optional, List
from development.database import SQLiteManager
import pyperclip

class Occurrence:
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = None,
        phone: str = None,
        highway: str = None,
        km: int = None,
        direction: str = None,
        vehicle: str = None,
        color: str = None,
        license_plate: str = None,
        problem: str = None,
        occupantes: str = None,
        local: str = None,
        reference_point: str = None,
        observations: str = None,
        is_vehicle: bool = True,
    ):
        self.id = id
        self.name = name
        self.phone = phone
        self.highway = highway
        self.km = km
        self.direction = direction
        self.vehicle = vehicle
        self.color = color
        self.license_plate = license_plate
        self.occupantes = occupantes
        self.problem = problem
        self.local = local
        self.reference_point = reference_point
        self.observations = observations
        self.is_vehicle = is_vehicle
        self.db_path = "app/database/database.db"

        self.create_table()

    def create_table(self):
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        with SQLiteManager(db_name=self.db_path) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS occurrences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    highway TEXT,
                    km INTEGER,
                    direction TEXT,
                    vehicle TEXT,
                    color TEXT,
                    license_plate TEXT,
                    problem TEXT,
                    occupantes TEXT,
                    local TEXT,
                    reference_point TEXT,
                    observations TEXT,
                    is_vehicle BOOLEAN
                );
            """)

    def clipboard(self):
        observacao = f"OBS: {self.observations}\n\n" if self.observations else ""

        if self.is_vehicle:
            texto = f"{observacao}RODOVIA: {self.highway}\nKM: {self.km}\nSENTIDO: {self.direction}\n\nVEÍCULO: {self.vehicle}\nCOR: {self.color}\nPLACA: {self.license_plate}\n\nPROBLEMA: {self.problem}\nOCUPANTES: {self.occupantes}\nENCONTRA-SE: {self.local}\n\nPONTO DE REFERÊNCIA: {self.reference_point}"
        else:
            texto = f"{observacao}RODOVIA: {self.highway}\nKM: {self.km}\nSENTIDO: {self.direction}\n\nPROBLEMA: {self.problem}\nENCONTRA-SE: {self.local}\n\nPONTO DE REFERÊNCIA: {self.reference_point}"

        pyperclip.copy(texto)
    
    def save(self) -> int:
        vehicle = self.vehicle if self.is_vehicle else None
        color = self.color if self.is_vehicle else None
        license_plate = self.license_plate if self.is_vehicle else None
        occupantes = self.occupantes if self.is_vehicle else None

        query = """
        INSERT INTO occurrences (
            name, phone, highway, km, direction, vehicle, color, 
            license_plate, problem, occupantes, local, reference_point, observations, is_vehicle
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params: Tuple = (
            self.name, self.phone, self.highway, self.km, self.direction,
            vehicle, color, license_plate, self.problem,
            occupantes, self.local, self.reference_point, self.observations, self.is_vehicle
        )
        return self.execute(query, params, fetch_id=True)

    def update(self):
        if self.id is None:
            raise ValueError("ID da ocorrência não pode ser None para atualizar.")
        
        vehicle = self.vehicle if self.is_vehicle else None
        color = self.color if self.is_vehicle else None
        license_plate = self.license_plate if self.is_vehicle else None
        occupantes = self.occupantes if self.is_vehicle else None

        query = """
        UPDATE occurrences
        SET name=?, phone=?, highway=?, km=?, direction=?, vehicle=?, color=?, 
            license_plate=?, problem=?, occupantes=?, local=?, reference_point=?, observations=?, is_vehicle=?
        WHERE id=?
        """
        params: Tuple = (
            self.name, self.phone, self.highway, self.km, self.direction,
            vehicle, color, license_plate, self.problem,
            occupantes, self.local, self.reference_point, self.observations, self.is_vehicle, self.id
        )
        self.execute(query, params)

    def delete(self):
        if self.id is None:
            raise ValueError("ID da ocorrência não pode ser None para deletar.")

        query = "DELETE FROM occurrences WHERE id=?"
        self.execute(query, (self.id,))

    def execute(self, query: str, params: Tuple = (), fetch_id: bool = False) -> Optional[int]:
        with SQLiteManager(db_name=self.db_path) as db:
            db.execute(query, params)
            if fetch_id:
                return db.cursor.lastrowid
        return None

    def searchPagination(self, search: Optional[str] = None, page: int = 1, rows: int = 15) -> List['Occurrence']:
        offset = (page - 1) * rows
        query = """
        SELECT id, name, phone, highway, km, direction, vehicle, color, license_plate, 
               problem, occupantes, local, reference_point, observations, is_vehicle
        FROM occurrences
        """
        
        params = ()
        
        if search:
            query += """
            WHERE name LIKE ? 
            OR phone LIKE ? 
            OR highway LIKE ? 
            OR CAST(km AS TEXT) LIKE ? 
            OR vehicle LIKE ? 
            OR license_plate LIKE ?
            """
            params = ('%' + search + '%',) * 6
        
        query += " LIMIT ? OFFSET ?"
        params += (rows, offset)

        with SQLiteManager(db_name=self.db_path) as db:
            db.execute(query, params)
            results = db.cursor.fetchall()

        occurrences = [
            Occurrence(
                id=row[0],
                name=row[1],
                phone=row[2],
                highway=row[3],
                km=row[4],
                direction=row[5],
                vehicle=row[6],
                color=row[7],
                license_plate=row[8],
                problem=row[9],
                occupantes=row[10],
                local=row[11],
                reference_point=row[12],
                observations=row[13],
                is_vehicle=row[14]
            )
            for row in results
        ]

        return occurrences
