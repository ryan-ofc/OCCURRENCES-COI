import sqlite3
from typing import List, Tuple, Any

class SQLiteManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None  # Inicializa a conexão como None
        self.cursor = None  # Inicializa o cursor como None

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
