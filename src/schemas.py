from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Ingredients(BaseModel):
    name: str = Field(description="Name of the ingredient")
    quantity: Optional[str] = Field(
        None, description="Amount or measurement of the ingredient"
    )


class Dish(BaseModel):
    dish_name: str = Field(description="Name of the dish")
    quantity: Optional[str] = Field(
        None, description="Serving size or amount of the dish"
    )
    ingredients: List[Ingredients] = Field(
        description="List of ingredient items for this dish"
    )


class Dishes(BaseModel):
    dishes: List[Dish] = Field(
        description="List of dishes with their quantities and items"
    )


class Nutrition(BaseModel):
    dish_names: str = Field(description="Name of the food item")
    calories: Optional[float] = Field(None, description="Calories per serving")
    protein_g: Optional[float] = Field(None, description="Protein in grams")
    carbs_g: Optional[float] = Field(None, description="Carbohydrates in grams")
    fat_g: Optional[float] = Field(None, description="Fat in grams")


class NutritionList(BaseModel):
    dishes: List[Nutrition]


class EstimateRequest(BaseModel):
    meal: str


class EstimateResponse(BaseModel):
    ingredients: Dict[str, Any]
    nutrition: Dict[str, Any]


class NutriBenchRecord(BaseModel):
    meal_description: str = Field(..., description="Original user meal text")
    carb: float = Field(..., description="Total carbohydrates in grams")
    fat: float = Field(..., description="Total fat in grams")
    energy: float = Field(..., description="Total energy in kilocalories")
    protein: float = Field(..., description="Total protein in grams")
    country: Optional[str] = None
    serving_type: Optional[Literal["metric", "natural"]] = None
