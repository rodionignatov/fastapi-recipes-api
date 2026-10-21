from pydantic import BaseModel, Field
from typing import List, Optional


class IngredientBase(BaseModel):
    name: str = Field(..., description="Название ингредиента", example="Мука")
    quantity: Optional[str] = Field(None, description="Количество", example="200 г")


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда", example="Блины")
    cooking_time: int = Field(..., description="Время приготовления (мин)", example=30)
    description: str = Field(..., description="Текстовое описание")


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate] = Field(default_factory=list)


class RecipeListItem(RecipeBase):
    id: int
    views: int = Field(0, description="Количество просмотров")

    class Config:
        from_attributes = True


class RecipeDetail(RecipeBase):
    id: int
    views: int
    ingredients: List[Ingredient]

    class Config:
        from_attributes = True