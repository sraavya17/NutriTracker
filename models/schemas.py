from pydantic import BaseModel
from typing import List, Optional

class UserPreferences(BaseModel):
    age: int
    gender: str
    goal: Optional[str] = None
    diet_preference: Optional[str] = None
    allergies: List[str] = []
    calorie_target: Optional[int] = None

class FoodRequest(BaseModel):
    food_items: List[str]
    user_preferences: UserPreferences

class NutrientComparison(BaseModel):
    nutrient: str
    consumed: float
    required: float
    status: str  

class NutritionResponse(BaseModel):
    summary: str
    comparison: List[NutrientComparison]
    recommendations: List[str]