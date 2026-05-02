#!/bin/bash

# Setup script for AI-Based Personal Fitness Assistant

echo "=========================================="
echo "  Fitness Assistant - Setup Script"
echo "=========================================="
echo ""

# Step 1: Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Step 2: Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Generate dataset
echo "📊 Generating training dataset..."
cd data
python3 generate_dataset.py
cd ..

# Step 5: Train ML model
echo "🤖 Training ML model..."
cd models
python3 -c "
import sys
sys.path.insert(0, '../data')
from generate_dataset import generate_fitness_dataset
from calorie_model import train_and_save_model
import os

# Generate dataset
df = generate_fitness_dataset(500)
df.to_csv('../data/fitness_dataset.csv', index=False)

# Train model
train_and_save_model()
"
cd ..

echo ""
echo "=========================================="
echo "  Setup Complete! ✅"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "  python3 app/app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
