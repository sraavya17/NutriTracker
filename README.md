# 🥗 NutriTracker

**Your Personal Nutrition Assistant**

NutriTracker is a web-based nutrition analysis tool that helps you track your daily food intake and provides personalized dietary recommendations based on your health goals and nutritional requirements.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## ✨ Features

- 🔍 **Food Data Retrieval**: Integration with USDA FoodData Central API for comprehensive nutrition information
- 🤖 **AI-Powered Analysis**: Uses Groq's LLaMA model for intelligent nutrition analysis and recommendations
- 👤 **Personalized Recommendations**: Tailored advice based on age, gender, health goals, and dietary preferences
- 📊 **Visual Nutrition Dashboard**: Interactive web interface with progress bars and status indicators
- 🎯 **Goal-Oriented Tracking**: Support for weight loss, weight gain, muscle gain, and maintenance goals
- 🌱 **Diet Preferences**: Accommodates various dietary preferences (vegetarian, vegan, keto, paleo, mediterranean)
- ⚠️ **Allergy Management**: Tracks and considers food allergies in recommendations

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **USDA FoodData Central API** - Comprehensive nutrition database
- **Groq API** - Advanced language model for nutrition analysis

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **JavaScript (ES6+)** - Dynamic frontend functionality
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icon library
- **Axios** - HTTP client for API calls

## 📁 Project Structure

```
NutriTracker/
├── models/
│   └── schemas.py              # Pydantic data models
├── services/
│   ├── nutrition.py            # USDA API integration
│   └── groq_client.py          # Groq LLM integration
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling
│   └── js/
│       └── main.js             # Frontend logic
├── templates/
│   └── index.html              # Main web interface
├── main.py                     # FastAPI application entry point
├── nutritional_goals.json     # Nutritional reference data
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- USDA FoodData Central API Key
- Groq API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sraavya17/NutriTracker.git
   cd NutriTracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   USDA_API_KEY=your_usda_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

   **Get your API keys:**
   - USDA API Key: [Register at FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html)
   - Groq API Key: [Sign up at Groq Console](https://console.groq.com/)

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8000`

## 🎯 Usage

### Web Interface

1. **Enter Food Items**: Add the foods you've consumed today
2. **Personal Information**: Fill in your age, gender, and preferences
3. **Health Goals**: Select your nutrition goal (optional)
4. **Diet Preferences**: Choose your dietary restrictions (optional)
5. **Analyze**: Click "Analyze Nutrition" to get your report

### API Endpoints

#### `POST /analyze`

Analyze nutrition data for given food items and user preferences.

**Request Body:**
```json
{
  "food_items": ["apple", "banana", "chicken breast"],
  "user_preferences": {
    "age": 25,
    "gender": "female",
    "goal": "weight_loss",
    "diet_preference": "vegetarian",
    "allergies": ["peanuts"],
    "calorie_target": 1800
  }
}
```

**Response:**
```json
{
  "summary": "Based on your food intake...",
  "comparison": [
    {
      "nutrient": "Protein",
      "consumed": 45.2,
      "required": 60.0,
      "status": "low"
    }
  ],
  "recommendations": [
    "Add more protein-rich foods to your diet",
    "Consider having Greek yogurt as a snack"
  ]
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `USDA_API_KEY` | API key for USDA FoodData Central | Yes |
| `GROQ_API_KEY` | API key for Groq language model | Yes |

### Nutritional Goals

The application uses age and gender-specific nutritional guidelines stored in `nutritional_goals.json`. This file contains recommended daily values for various nutrients across different demographic groups.

## 🚗 Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Dependencies

**Core Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `jinja2` - Template engine
- `python-dotenv` - Environment variable management
- `requests` - HTTP library for API calls
- `groq` - Groq API client


## 👤 Author

**Sraavya**
- GitHub: [@sraavya17](https://github.com/sraavya17)

## 🙏 Acknowledgments

- [USDA FoodData Central](https://fdc.nal.usda.gov/) for comprehensive nutrition data
- [Groq](https://groq.com/) for AI-powered nutrition analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Bootstrap](https://getbootstrap.com/) for the responsive UI components

---

**⭐ Star this repository if you find it helpful!**