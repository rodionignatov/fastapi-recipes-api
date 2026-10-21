from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from database import init_db, get_db
from models import Recipe, Ingredient
from schemas import RecipeCreate, RecipeListItem, RecipeDetail

app = FastAPI(title="Кулинарная книга API", version="1.0.0")


@app.on_event("startup")
async def startup():
    await init_db()


@app.get('/recipes', response_model=List[RecipeListItem], tags=["Recipes"])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    """
    Список всех рецептов, отсортированных по популярности (views),
    затем по времени приготовления.
    """
    result = await db.execute(
        select(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
    )
    return result.scalars().all()


@app.get('/recipes/{recipe_id}', response_model=RecipeDetail, tags=["Recipes"])
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """
    Детальная информация о рецепте. Увеличивает счётчик просмотров.
    """
    result = await db.execute(
        select(Recipe)
        .options(selectinload(Recipe.ingredients))
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)

    return recipe


@app.post('/recipes', response_model=RecipeDetail, status_code=201, tags=["Recipes"])
async def create_recipe(recipe_data: RecipeCreate, db: AsyncSession = Depends(get_db)):
    """
    Создать новый рецепт с ингредиентами.
    """
    recipe = Recipe(
        title=recipe_data.title,
        cooking_time=recipe_data.cooking_time,
        description=recipe_data.description,
    )
    recipe.ingredients = [
        Ingredient(name=i.name, quantity=i.quantity)
        for i in recipe_data.ingredients
    ]
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)

    result = await db.execute(
        select(Recipe)
        .options(selectinload(Recipe.ingredients))
        .where(Recipe.id == recipe.id)
    )
    return result.scalar_one()