import psycopg2.extras
from database import get_connection

class IngredientRepository:
    def find_by_name(self, name: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM ingredients WHERE LOWER(name) = LOWER(%s)", (name,))
        ingredient = cur.fetchone()
        cur.close()
        conn.close()
        return ingredient

    def save(self, name: str, default_unit: str = None):
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

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM ingredients ORDER BY name ASC")
        ingredients = cur.fetchall()
        cur.close()
        conn.close()
        return ingredients