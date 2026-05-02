"""
Generate sample dataset for calorie prediction model training
"""

import pandas as pd
import numpy as np

def generate_fitness_dataset(n_samples=500):
    """
    Generate synthetic dataset for calorie prediction
    Features: age, height, weight, gender, activity_level
    Target: daily_calorie_requirement
    """
    np.random.seed(42)

    data = {
        'age': np.random.randint(18, 65, n_samples),
        'height': np.random.normal(170, 10, n_samples),  # cm
        'weight': np.random.normal(75, 15, n_samples),   # kg
        'gender': np.random.choice([0, 1], n_samples),   # 0: Female, 1: Male
        'activity_level': np.random.choice([1, 1.375, 1.55, 1.725, 1.9], n_samples)  # Activity multiplier
    }

    df = pd.DataFrame(data)

    # Calculate BMR using Mifflin-St Jeor equation
    df['bmr'] = np.where(
        df['gender'] == 1,
        (10 * df['weight']) + (6.25 * df['height']) - (5 * df['age']) + 5,
        (10 * df['weight']) + (6.25 * df['height']) - (5 * df['age']) - 161
    )

    # Daily calorie requirement = BMR * Activity Level
    df['daily_calories'] = df['bmr'] * df['activity_level']

    # Add some noise for realism
    df['daily_calories'] += np.random.normal(0, 50, n_samples)

    # Drop bmr as it's intermediate
    df = df.drop('bmr', axis=1)

    return df

if __name__ == '__main__':
    df = generate_fitness_dataset(500)
    df.to_csv('fitness_dataset.csv', index=False)
    print(f"Dataset generated with shape: {df.shape}")
    print("\nDataset preview:")
    print(df.head(10))
    print("\nDataset statistics:")
    print(df.describe())
