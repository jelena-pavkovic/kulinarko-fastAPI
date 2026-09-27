from abc import ABC, abstractmethod
import psycopg2.extras
from database import get_connection

class DatabaseTarget(ABC):
    @abstractmethod
    def find_by_name(self, name: str) -> dict:
        pass

    @abstractmethod
    def save_ingredient(self, name: str, default_unit: str = None) -> dict:
        pass

class PostgresDatabaseAdapter(DatabaseTarget):
    def find_by_name(self, name: str) -> dict:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM ingredients WHERE name = %s", (name,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def save_ingredient(self, name: str, default_unit: str = None) -> dict:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO ingredients (name, default_unit) VALUES (%s, %s) RETURNING *",
            (name, default_unit)
        )
        new_ingredient = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_ingredient