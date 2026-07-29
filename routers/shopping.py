from fastapi import APIRouter, HTTPException
from database import get_connection
from pydantic import BaseModel
import psycopg2.extras

router = APIRouter()

class ShoppingItemCreate(BaseModel):
    name: str
    quantity: float
    unit: str
    ingredient_id: int = None

@router.get("")

def get_shopping_list():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT si.* FROM shopping_items si
        JOIN shopping_lists sl ON si.shopping_list_id = sl.id
        ORDER BY si.id ASC
    """)
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items

@router.post("/items")
def add_item(item: ShoppingItemCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM shopping_lists LIMIT 1")
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO shopping_lists (name) VALUES ('Lista za kupovinu') RETURNING id")
        list_id = cur.fetchone()[0]
    else:
        list_id = row[0]
    cur.execute(
        "INSERT INTO shopping_items (shopping_list_id, name, quantity, unit, ingredient_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (list_id, item.name, item.quantity, item.unit, item.ingredient_id)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Stavka dodana"}

@router.put("/items/{item_id}")
def toggle_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE shopping_items SET is_checked = NOT is_checked WHERE id = %s",
        (item_id,)
    )
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Stavka nije pronađena")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Stavka ažurirana"}

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM shopping_items WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Stavka obrisana"}

@router.delete("/checked")
def delete_checked():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM shopping_items WHERE is_checked = TRUE")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Čekirane stavke obrisane"}

@router.delete("/all")
def delete_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM shopping_items")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Sve stavke obrisane"}