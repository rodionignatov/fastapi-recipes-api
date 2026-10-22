from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class IngredientBase(BaseModel):
    name: str = Field(..., description="Название ингредиента", examples=["Мука"])
    quantity: Optional[str] = Field(None, description="Количество", examples=["200 г"])


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда", examples=["Блины"])
    cooking_time: int = Field(
        ..., description="Время приготовления (мин)", examples=[30]
    )
    description: str = Field(..., description="Текстовое описание")


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate] = Field(default_factory=list)


class RecipeListItem(RecipeBase):
    id: int
    views: int = Field(0, description="Количество просмотров")
    model_config = ConfigDict(from_attributes=True)


class RecipeDetail(RecipeBase):
    id: int
    views: int
    ingredients: List[Ingredient]
    model_config = ConfigDict(from_attributes=True)
