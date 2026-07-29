from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import recipes, categories, ingredients, shopping

app = FastAPI(title="Kulinarko API")

app.include_router(recipes.router, prefix="/api/recipes", tags=["recepti"])
app.include_router(categories.router, prefix="/api/categories", tags=["kategorije"])
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["sastojci"])
app.include_router(shopping.router, prefix="/api/shopping", tags=["kupovina"])

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
@app.get("/")

def root():
    return {"status": "Kulinarko API radi"}
