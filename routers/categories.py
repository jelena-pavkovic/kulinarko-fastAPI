from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel
from typing import Optional
import psycopg2.extras

router = APIRouter()

@router.get("")
def get_categories():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM categories ORDER BY name ASC")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return categories


class CategoryCreate(BaseModel):
    name: str
    icon: Optional[str] = None

@router.post("")
def create_category(category: CategoryCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO categories (name, icon) VALUES (%s, %s) RETURNING id",
        (category.name, category.icon)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Kategorija dodana"}

@router.put("/{category_id}")
def update_category(category_id: int, category: CategoryCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE categories SET name = %s, icon = %s WHERE id = %s",
        (category.name, category.icon, category_id)
    )
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Kategorija izmenjena"}

@router.delete("/{category_id}")
def delete_category(category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE id = %s", (category_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Kategorija nije pronađena")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Kategorija obrisana"}
