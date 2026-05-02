@echo off
REM Setup script for AI-Based Personal Fitness Assistant (Windows)

echo.
echo ==========================================
echo   Fitness Assistant - Windows Setup
echo ==========================================
echo.

REM Step 1: Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Step 2: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Step 3: Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Step 4: Generate dataset
echo Generating training dataset...
cd data
python generate_dataset.py
cd ..

REM Step 5: Train ML model
echo Training ML model...
cd models
python -c "import sys; sys.path.insert(0, '../data'); from generate_dataset import generate_fitness_dataset; from calorie_model import train_and_save_model; df = generate_fitness_dataset(500); df.to_csv('../data/fitness_dataset.csv', index=False); train_and_save_model()"
cd ..

echo.
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To start the application, run:
echo   python app/app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
pause
