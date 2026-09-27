from fastapi import APIRouter
from .database_adapter import PostgresDatabaseAdapter 
from .ingredient_factory import IngredientFactory

router = APIRouter()
db_adapter = PostgresDatabaseAdapter()       
factory = IngredientFactory(db_adapter)   

@router.get("")
def get_ingredients():
    return db_adapter.get_all() 

@router.post("")
def create_ingredient(name: str, default_unit: str = None):
    ingredient = factory.get_or_create(name, default_unit)
    return {"id": ingredient.item_id, "message": "Sastojak dodan"}


"""
from fastapi import APIRouter
from .ingredient_repository import IngredientRepository
from .ingredient_factory import IngredientFactory

router = APIRouter()
repository = IngredientRepository()
factory = IngredientFactory(repository)

@router.get("")
def get_ingredients():
    return repository.get_all()

@router.post("")
def create_ingredient(name: str, default_unit: str = None):
    ingredient = factory.get_or_create(name, default_unit)
    return {"id": ingredient["id"], "message": "Sastojak dodan"}
"""

"""
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
"""