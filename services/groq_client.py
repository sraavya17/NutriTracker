from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

def analyze_nutrition(food_data, user_preferences, nutrient_data):
    """Analyze nutrition using Groq API"""
    completion = client.chat.completions.create(
        model="llama-3.3-70B-Versatile",
        messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a nutrition assistant. "
                            "Always respond with ONLY valid JSON (no extra text, no explanations). "
                            "Do not include markdown formatting or code blocks. "
                            "If data is missing, infer reasonably but still follow the JSON schema strictly."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"""
                Food intake data: {food_data}
                User preferences: {user_preferences}
                Nutrient goals: {nutrient_data}

                Return ONLY valid JSON in this structure:
                {{
                "summary": "A short paragraph summarizing nutrient intake",
                "comparison": [
                    {{
                    "nutrient": "Protein",
                    "consumed": 60,
                    "required": 75,
                    "status": "low"
                    }},
                    {{
                    "nutrient": "Carbohydrate",
                    "consumed": 200,
                    "required": 180,
                    "status": "ok"
                    }}
                ],
                "recommendations": [
                    "Add a high-protein snack like Greek yogurt",
                    "Reduce refined carbs and replace with whole grains"
                ]
                }}
                """
                    }
                ]

    )
    content = completion.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # fallback to avoid FastAPI 500
        return {
            "summary": "Error parsing response",
            "comparison": [],
            "recommendations": []
        }
