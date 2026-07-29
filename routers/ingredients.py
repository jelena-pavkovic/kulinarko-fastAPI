from fastapi import APIRouter
from database import get_connection
import psycopg2.extras

router = APIRouter()

@router.get("")

def get_ingredients():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM ingredients ORDER BY name ASC")
    ingredients = cur.fetchall()
    cur.close()
    conn.close()
    return ingredients

@router.post("")

def create_ingredient(name: str, default_unit: str = None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ingredients (name, default_unit) VALUES (%s, %s) RETURNING id",
        (name, default_unit)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Sastojak dodan"}