import sqlite3
from development.utils.occurrence import Occurrence
from typing import Optional, List, Tuple, Any
from math import ceil


class ResponseSearch:
    def __init__(
        self,
        page: int = None,
        total_pages: int = None,
        total_rows: int = None,
        data: List[Occurrence] = None,
    ):
        self.page = page
        self.total_pages = total_pages
        self.total_rows = total_rows
        self.data = data


class SQLiteManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Abre a conexão e retorna o próprio objeto para uso com 'with'."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self  # Retorna a própria instância da classe

    def __exit__(self, exc_type, exc_value, traceback):
        """Fecha a conexão automaticamente quando sai do bloco 'with'."""
        if self.conn:
            if exc_type is None:  # Se não houve erro, faz commit
                self.conn.commit()
            self.conn.close()

    def execute(self, query: str, params: Tuple = ()) -> None:
        """Executa uma query sem retorno (INSERT, UPDATE, DELETE)."""
        self.cursor.execute(query, params)

    def fetchone(self, query: str, params: Tuple = ()) -> Tuple[Any]:
        """Executa uma query e retorna um único resultado."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query: str, params: Tuple = ()) -> List[Tuple[Any]]:
        """Executa uma query e retorna todos os resultados."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def create_table(self, table_name: str, columns: str) -> None:
        """Cria uma tabela no banco de dados."""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute(query)

    def searchPagination(
        self, search: Optional[str] = None, page: int = 1, rows: int = 15
    ) -> ResponseSearch:
        offset = (page - 1) * rows

        base_query = """
        SELECT id, name, phone, highway, km, direction, vehicle, color, license_plate, 
            problem, occupantes, local, reference_point, observations, is_vehicle
        FROM occurrences
        """

        count_query = "SELECT COUNT(*) FROM occurrences"
        params = ()

        if search:
            filter_clause = """
            WHERE name LIKE ? 
            OR phone LIKE ? 
            OR highway LIKE ? 
            OR CAST(km AS TEXT) LIKE ? 
            OR vehicle LIKE ? 
            OR license_plate LIKE ?
            """
            base_query += filter_clause
            count_query += filter_clause
            params = ("%" + search + "%",) * 6

        base_query += " LIMIT ? OFFSET ?"
        params += (rows, offset)

        with SQLiteManager(db_name=self.db_path) as db:
            # Obtendo total de registros
            db.execute(count_query, params[:6])
            total_rows = db.cursor.fetchone()[0]

            # Executando a query principal
            db.execute(base_query, params)
            results = db.cursor.fetchall()

        total_pages = ceil(total_rows / rows) if total_rows > 0 else 1

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
                is_vehicle=row[14],
            )
            for row in results
        ]

        return ResponseSearch(page=page,total_pages=total_pages,total_rows=total_rows, data=occurrences)
