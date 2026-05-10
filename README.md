# 💪 AI-Based Personal Fitness Assistant


An intelligent full-stack web application that leverages machine learning and rule-based systems to generate personalized workout plans, diet recommendations, and adaptive fitness guidance.

## 🚀 Overview

The AI-Based Personal Fitness Assistant is designed as a real-world application that helps users achieve their fitness goals through data-driven insights.

It combines machine learning, fitness science, and software engineering to deliver:

- Personalized workout routines
- Budget-friendly diet plans (Indian-focused)
- Calorie prediction using ML
- Progress tracking and analytics
- Explainable AI-based recommendations

## ✨ Key Features

### 🔹 Smart Calorie Prediction

- Random Forest regression model for calorie estimation
- Backup using Mifflin-St Jeor equation
- Goal-based calorie adjustment (fat loss / muscle gain / maintenance)

### 🔹 Personalized Workout Plans

- Push/Pull/Legs (PPL) split (gym users)
- Full-body workouts (home users)
- Exercise selection based on experience level
- Structured sets, reps, and rest intervals
- Progressive overload recommendations

### 🔹 Diet Plan Generation

- Uses real Indian food items (paneer, dal, soya, etc.)
- Budget-aware meal planning
- Protein-focused diet suggestions
- Vegetarian & non-vegetarian options
- Daily nutrition breakdown

### 🔹 Progress Tracking

- Weight logging over time
- Trend visualization
- Progress insights and summaries
- Notes for each entry

### 🔹 AI-Based Recommendations

- Detects progress trends and plateaus
- Suggests calorie adjustments
- Recommends cardio or deload phases
- Provides explainable reasoning

### 🔹 Explainable AI

- Displays why recommendations were generated
- Highlights influencing factors
- Builds user trust through transparency

## 🧠 Tech Stack

### Backend

- Flask
- SQLite
- SQLAlchemy
- Flask-Session

### Machine Learning

- scikit-learn
- Random Forest Regressor
- Pandas, NumPy

### Frontend

- HTML5, CSS3, JavaScript (Vanilla)
- Responsive custom UI

## 📁 Project Structure

```
fitness_assistant/
├── app/
│   ├── templates/
│   ├── static/
│   ├── models/
│   ├── utils/
│   └── app.py
├── data/
├── models/
├── notebooks/
├── requirements.txt
├── setup.sh / setup.bat
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

#### Quick Setup (Recommended)

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

#### Manual Setup

```bash
python3 -m venv venv

# Activate
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

pip install -r requirements.txt

# Generate dataset
cd data
python3 generate_dataset.py
cd ..

# Train model
cd models
python3 calorie_model.py
cd ..
```

### Run the App

```bash
python3 app/app.py
```

Open:

- http://localhost:5000

## 📊 Database Schema

### Users

- id, username, email
- age, height, weight
- fitness goal, experience level
- diet preference, budget
- created_at

### Fitness Plans

- user_id
- calories, protein
- workout_plan (JSON)
- diet_plan (JSON)

### Progress Logs

- user_id
- weight, timestamp
- notes

### Recommendations

- type, message, action
- created_at

## 🤖 Machine Learning Details

- Model: Random Forest Regressor
- Features: Age, Height, Weight, Gender, Activity Level
- Target: Daily Calories
- Accuracy: ~0.92 R²

## 🔌 API Endpoints

### Auth

- POST `/api/register`
- POST `/api/login`
- POST `/api/logout`

### User

- GET `/api/user/<id>`

### Plans

- POST `/api/generate-plan`
- GET `/api/plans/<id>`

### Progress

- POST `/api/log-weight`
- GET `/api/progress/<id>`

### Recommendations

- GET `/api/recommendations/<id>`

## 💡 How It Works

1. User inputs profile data
2. ML model predicts calorie needs
3. System generates workout + diet plan
4. User logs progress
5. AI analyzes trends and updates recommendations

## 🎯 Highlights

- End-to-end ML pipeline (training → deployment)
- Real-world problem solving (fitness + nutrition)
- Explainable AI decisions
- Clean modular architecture
- Scalable backend design

## 🚀 Deployment

### Render / Railway

- Connect GitHub repo
- Install dependencies
- Start:

```bash
python app/app.py
```

### Production (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app.app:app
```

## 📈 Future Improvements

- LLM-based fitness chatbot
- Food image recognition
- Advanced analytics dashboard
- Social features
- Mobile app integration
- Wearable device support

## 🐛 Troubleshooting

### Flask not found

```bash
pip install -r requirements.txt
```

### Database locked

Restart application

### Model missing

```bash
cd data && python3 generate_dataset.py
cd models && python3 calorie_model.py
```

## 📄 License

This project is intended for educational and demonstration purposes.

## 👨‍💻 Author

Developed as a full-stack machine learning application demonstrating real-world AI use cases in fitness and health.

## ❓ FAQ

### Can I modify workouts?

Yes → edit `fitness_generators.py`

### Is the ML model accurate?

~92% R² (approximation, not medical advice)

### Can I deploy it?

Yes — use Render, Railway, or VPS

## 📞 Support

Refer to code comments or troubleshooting section for help.

---

**💪 Build. Track. Improve.**
