"""
Flask Application for AI-Based Personal Fitness Assistant
Main application with all routes and business logic
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os
import sys

# Set up paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Use relative imports within app package
from .models.db import db, User, FitnessPlan, ProgressLog, Recommendation
from .utils.fitness_generators import WorkoutPlanGenerator, DietPlanGenerator, AIRecommendationEngine

# Dynamic import for calorie model from parent models folder
import importlib.util
calorie_model_path = os.path.join(parent_dir, 'models', 'calorie_model.py')
spec = importlib.util.spec_from_file_location("calorie_model", calorie_model_path)
calorie_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calorie_module)
CaloriePredictor = calorie_module.CaloriePredictor

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-fitness-app-2024'

# Initialize extensions
db.init_app(app)

# Load ML model
calorie_predictor = CaloriePredictor()
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'calorie_predictor.pkl')

def load_model():
    """Load the calorie prediction model"""
    global calorie_predictor
    if os.path.exists(model_path):
        try:
            calorie_predictor.load(model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    return False

# Helper functions
def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation"""
    if gender.lower() == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmr

def calculate_protein(weight, goal):
    """Calculate protein requirement based on goal"""
    if goal == 'muscle_gain':
        return weight * 2.2  # 2.2g per kg for muscle gain
    elif goal == 'fat_loss':
        return weight * 1.8  # 1.8g per kg for fat loss
    else:
        return weight * 1.6  # 1.6g per kg for maintenance

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validate input
        if not data.get('username') or not data.get('email'):
            return jsonify({'error': 'Username and email required'}), 400

        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            age=int(data['age']),
            height=float(data['height']),
            weight=float(data['weight']),
            gender=data['gender'],
            fitness_goal=data['fitness_goal'],
            experience_level=data['experience_level'],
            diet_preference=data['diet_preference'],
            daily_budget=float(data['daily_budget']),
            workout_preference=data['workout_preference']
        )

        db.session.add(user)
        db.session.commit()

        # Store user ID in session
        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({
            'success': True,
            'user_id': user.id,
            'message': 'Login successful'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    """Generate fitness and diet plan for user"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401

        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Calculate calories using ML model
        gender_encoded = 1 if user.gender.lower() == 'male' else 0
        activity_level = request.get_json().get('activity_level', 1.55)  # Default: moderate activity

        try:
            daily_calories = calorie_predictor.predict(
                age=user.age,
                height=user.height,
                weight=user.weight,
                gender=gender_encoded,
                activity_level=activity_level
            )
        except:
            # Fallback to manual calculation if model fails
            bmr = calculate_bmr(user.weight, user.height, user.age, user.gender)
            daily_calories = bmr * activity_level

        # Adjust calories based on goal
        if user.fitness_goal == 'fat_loss':
            daily_calories *= 0.85
        elif user.fitness_goal == 'muscle_gain':
            daily_calories *= 1.10

        # Calculate protein requirement
        daily_protein = calculate_protein(user.weight, user.fitness_goal)

        # Generate plans
        workout_gen = WorkoutPlanGenerator()
        diet_gen = DietPlanGenerator()

        workout_plan = workout_gen.generate_plan(
            experience_level=user.experience_level,
            goal=user.fitness_goal,
            workout_preference=user.workout_preference
        )

        diet_plan = diet_gen.generate_plan(
            daily_calories=daily_calories,
            protein_needed=daily_protein,
            budget=user.daily_budget,
            diet_preference=user.diet_preference
        )

        # Store plan in database
        fitness_plan = FitnessPlan(
            user_id=user.id,
            daily_calories=daily_calories,
            daily_protein=daily_protein,
            workout_plan=workout_plan,
            diet_plan=diet_plan
        )
        db.session.add(fitness_plan)
        db.session.commit()

        return jsonify({
            'success': True,
            'plan': {
                'daily_calories': round(daily_calories, 2),
                'daily_protein': round(daily_protein, 2),
                'workout_plan': workout_plan,
                'diet_plan': diet_plan,
                'explanation': {
                    'calories': f"Based on your BMR, activity level, and goal ({user.fitness_goal})",
                    'protein': f"Recommended protein for {user.fitness_goal}: {round(daily_protein, 1)}g/day"
                }
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/log-weight', methods=['POST'])
def log_weight():
    """Log user weight progress"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        weight = float(data['weight'])

        progress_log = ProgressLog(
            user_id=session['user_id'],
            weight=weight,
            notes=data.get('notes', '')
        )

        db.session.add(progress_log)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Weight logged successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<int:user_id>', methods=['GET'])
def get_progress(user_id):
    """Get user progress logs"""
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    logs = ProgressLog.query.filter_by(user_id=user_id).order_by(ProgressLog.logged_at).all()

    progress_data = [{
        'date': log.logged_at.strftime('%Y-%m-%d'),
        'weight': log.weight,
        'notes': log.notes
    } for log in logs]

    return jsonify({
        'success': True,
        'progress': progress_data,
        'total_logs': len(progress_data)
    }), 200

@app.route('/api/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get AI recommendations for user"""
    try:
        if 'user_id' not in session or session['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get progress logs
        logs = ProgressLog.query.filter_by(user_id=user_id).order_by(ProgressLog.logged_at).all()

        if len(logs) < 2:
            return jsonify({
                'success': True,
                'recommendations': [],
                'message': 'Need at least 2 weight logs for recommendations'
            }), 200

        # Calculate progress
        initial_weight = logs[0].weight
        current_weight = logs[-1].weight
        first_log_date = logs[0].logged_at
        weeks_elapsed = (datetime.utcnow() - first_log_date).days / 7

        # Get latest plan
        plan = FitnessPlan.query.filter_by(user_id=user_id).order_by(FitnessPlan.created_at.desc()).first()
        current_calories = plan.daily_calories if plan else 2000

        # Generate recommendations
        engine = AIRecommendationEngine()
        recommendations = engine.get_suggestions(
            current_weight=current_weight,
            initial_weight=initial_weight,
            goal=user.fitness_goal,
            weeks_elapsed=weeks_elapsed,
            current_calories=current_calories
        )

        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'progress_summary': {
                'weight_change': round(initial_weight - current_weight, 2),
                'weeks_elapsed': round(weeks_elapsed, 1),
                'logs_count': len(logs)
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans/<int:user_id>', methods=['GET'])
def get_plans(user_id):
    """Get user's fitness plans"""
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    plans = FitnessPlan.query.filter_by(user_id=user_id).order_by(FitnessPlan.created_at.desc()).all()

    plans_data = [plan.to_dict() for plan in plans]

    return jsonify({
        'success': True,
        'plans': plans_data,
        'total_plans': len(plans_data)
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': calorie_predictor.model is not None
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized!")

        # Load ML model
        if load_model():
            print("ML model loaded successfully!")
        else:
            print("WARNING: ML model not found. Using fallback calculations.")

    app.run(debug=True, host='0.0.0.0', port=5000)
