"""
Database models and initialization
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model to store user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)  # in cm
    weight = db.Column(db.Float, nullable=False)  # in kg
    gender = db.Column(db.String(10), nullable=False)  # 'Male' or 'Female'
    fitness_goal = db.Column(db.String(50), nullable=False)  # 'fat_loss', 'muscle_gain', 'maintenance'
    experience_level = db.Column(db.String(50), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    diet_preference = db.Column(db.String(20), nullable=False)  # 'veg' or 'non_veg'
    daily_budget = db.Column(db.Float, nullable=False)  # in INR
    workout_preference = db.Column(db.String(20), nullable=False)  # 'gym' or 'home'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    progress_logs = db.relationship('ProgressLog', backref='user', cascade='all, delete-orphan')
    plans = db.relationship('FitnessPlan', backref='user', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'gender': self.gender,
            'fitness_goal': self.fitness_goal,
            'experience_level': self.experience_level,
            'diet_preference': self.diet_preference,
            'daily_budget': self.daily_budget,
            'workout_preference': self.workout_preference
        }


class FitnessPlan(db.Model):
    """Store generated fitness plans"""
    __tablename__ = 'fitness_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    daily_calories = db.Column(db.Float, nullable=False)
    daily_protein = db.Column(db.Float, nullable=False)
    workout_plan = db.Column(db.JSON, nullable=False)  # Store as JSON
    diet_plan = db.Column(db.JSON, nullable=False)  # Store as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'daily_calories': self.daily_calories,
            'daily_protein': self.daily_protein,
            'workout_plan': self.workout_plan,
            'diet_plan': self.diet_plan,
            'created_at': self.created_at.isoformat()
        }


class ProgressLog(db.Model):
    """Log user progress over time"""
    __tablename__ = 'progress_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # in kg
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'weight': self.weight,
            'logged_at': self.logged_at.isoformat(),
            'notes': self.notes
        }


class Recommendation(db.Model):
    """Store AI recommendations for users"""
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'calorie_reduction', 'add_cardio', etc.
    message = db.Column(db.String(500), nullable=False)
    action = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_applied = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.recommendation_type,
            'message': self.message,
            'action': self.action,
            'created_at': self.created_at.isoformat(),
            'is_applied': self.is_applied
        }
