from fastapi import APIRouter, HTTPException
from database import get_connection
from models import RecipeCreate, RecipeUpdate

import psycopg2
import psycopg2.extras

router = APIRouter()

@router.get("")

def get_recipes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM recipes ORDER BY name ASC")
    recipes = cur.fetchall()
    cur.close()
    conn.close()

    return recipes

@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
    recipe = cur.fetchone()

    if recipe is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Recept nije pronađen")

    cur.execute("""
        SELECT ri.id, ri.ingredient_id, i.name, ri.quantity, ri.unit, ri.notes
        FROM recipe_ingredients ri
        JOIN ingredients i ON i.id = ri.ingredient_id
        WHERE ri.recipe_id = %s
    """, (recipe_id,))
    ingredients = cur.fetchall()

    cur.execute("""
        SELECT id, order_num, description
        FROM steps
        WHERE recipe_id = %s
        ORDER BY order_num ASC
    """, (recipe_id,))
    steps = cur.fetchall()

    cur.close()
    conn.close()

    recipe["ingredients"] = ingredients
    recipe["steps"] = steps

    return recipe

# DELETE /api/recipes/:id — briše recept

@router.delete("/{recipe_id}")

def delete_recipe(recipe_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Recept nije pronađen")

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Recept obrisan"}

def _get_or_create_ingredient(cur, name: str, unit: str) -> int:
    cur.execute("""
        INSERT INTO ingredients (name, default_unit)
        VALUES (%s, %s)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
    """, (name.strip(), unit))
    return cur.fetchone()[0]

def _save_ingredients(cur, recipe_id: int, ingredients):
    for ing in ingredients:
        ingredient_id = _get_or_create_ingredient(cur, ing.name, ing.unit)
        cur.execute("""
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (recipe_id, ingredient_id, ing.quantity, ing.unit, ing.notes))

def _save_steps(cur, recipe_id: int, steps):
    for step in steps:
        cur.execute("""
            INSERT INTO steps (recipe_id, order_num, description)
            VALUES (%s, %s, %s)
        """, (recipe_id, step.order_num, step.description))


@router.post("")
def create_recipe(recipe: RecipeCreate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO recipes (name, category_id, description, prep_time_min, servings)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (recipe.name, recipe.category_id, recipe.description, recipe.prep_time_min, recipe.servings))
        new_id = cur.fetchone()[0]

        _save_ingredients(cur, new_id, recipe.ingredients)
        _save_steps(cur, new_id, recipe.steps)

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

    return {"id": new_id, "message": "Recept dodan"}


@router.put("/{recipe_id}")
def update_recipe(recipe_id: int, recipe: RecipeUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE recipes
            SET name = %s, category_id = %s, description = %s,
                prep_time_min = %s, servings = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (recipe.name, recipe.category_id, recipe.description, recipe.prep_time_min, recipe.servings,
                recipe_id))

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recept nije pronađen")

        # najjednostavnija strategija: obriši stare pa upiši nove
        cur.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s", (recipe_id,))
        cur.execute("DELETE FROM steps WHERE recipe_id = %s", (recipe_id,))

        _save_ingredients(cur, recipe_id, recipe.ingredients)
        _save_steps(cur, recipe_id, recipe.steps)

        conn.commit()
    except HTTPException:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

    return {"message": "Recept ažuriran"}
