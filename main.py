from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.schemas import FoodRequest, NutritionResponse
from services.nutrition import get_nutrient_goals
from services.groq_client import analyze_nutrition

app = FastAPI(title="NutriTracker API", description="Personal Nutrition Assistant")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_model=NutritionResponse)
def analyze_food(request: FoodRequest):
    food_data, nutrient_data = get_nutrient_goals(request.food_items, request.user_preferences.dict())
    result = analyze_nutrition(food_data, request.user_preferences.dict(), nutrient_data)
    return result