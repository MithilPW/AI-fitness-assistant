"""
Fitness Plan Generation Utilities
- Workout plan generator
- Diet plan generator
- AI recommendations
"""

class WorkoutPlanGenerator:
    """Generate personalized workout plans"""

    EXERCISES_BY_LEVEL = {
        'beginner': {
            'chest': ['Push-ups', 'Bench Press (Light)', 'Dumbbell Flyes'],
            'back': ['Assisted Pull-ups', 'Rows (Machine)', 'Lat Pulldowns'],
            'legs': ['Squats (Bodyweight)', 'Lunges', 'Leg Press'],
            'shoulders': ['Shoulder Press (Light)', 'Lateral Raises', 'Pike Push-ups'],
            'arms': ['Dumbbell Curls', 'Tricep Dips', 'Hammer Curls'],
            'cardio': ['Walking', 'Stationary Cycling', 'Treadmill (Low speed)']
        },
        'intermediate': {
            'chest': ['Barbell Bench Press', 'Incline Dumbbell Press', 'Cable Flyes'],
            'back': ['Pull-ups', 'Barbell Rows', 'T-Bar Rows'],
            'legs': ['Barbell Squats', 'Romanian Deadlifts', 'Leg Press'],
            'shoulders': ['Overhead Press', 'Machine Shoulder Press', 'Face Pulls'],
            'arms': ['Barbell Curls', 'Close-Grip Bench Press', 'Cable Curls'],
            'cardio': ['Running', 'Jump Rope', 'Rowing Machine']
        },
        'advanced': {
            'chest': ['Competition Bench Press', 'Paused Bench Press', 'Board Press'],
            'back': ['Weighted Pull-ups', 'Deficit Deadlifts', 'Heavy Rows'],
            'legs': ['Competition Squats', 'Box Squats', 'Front Squats'],
            'shoulders': ['Push Press', 'Landmine Press', 'Heavy Laterals'],
            'arms': ['Weighted Dips', 'Barbell Curls (Heavy)', 'Weighted Vests'],
            'cardio': ['HIIT Training', 'Sprint Intervals', 'Battle Ropes']
        }
    }

    HOME_WORKOUT = {
        'chest': ['Push-ups', 'Diamond Push-ups', 'Wide Push-ups'],
        'back': ['Pull-up Bar (if available)', 'Reverse Snow Angels', 'Resistance Band Rows'],
        'legs': ['Bodyweight Squats', 'Lunges', 'Step-ups'],
        'shoulders': ['Pike Push-ups', 'Handstand Hold', 'Resistance Band Press'],
        'arms': ['Resistance Band Curls', 'Tricep Dips (Chair)', 'Plank Shoulder Taps'],
        'cardio': ['Jumping Jacks', 'Burpees', 'High Knees']
    }

    def generate_plan(self, experience_level, goal, workout_preference='gym'):
        """
        Generate a weekly workout plan

        Args:
            experience_level: 'beginner', 'intermediate', 'advanced'
            goal: 'fat_loss', 'muscle_gain', 'maintenance'
            workout_preference: 'gym' or 'home'

        Returns:
            dict with weekly plan
        """
        exercises = self.HOME_WORKOUT if workout_preference == 'home' else self.EXERCISES_BY_LEVEL.get(experience_level, {})

        # PPL split for gym, modified for home
        if workout_preference == 'gym':
            plan = {
                'Day 1 (Push)': {
                    'Chest': {'exercise': exercises.get('chest', ['Push-ups'])[0], 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    'Shoulders': {'exercise': exercises.get('shoulders', ['Pike Push-ups'])[0], 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                    'Triceps': {'exercise': exercises.get('arms', ['Tricep Dips'])[0], 'sets': 3, 'reps': '8-12', 'rest': '60s'},
                },
                'Day 2 (Pull)': {
                    'Back': {'exercise': exercises.get('back', ['Rows'])[0], 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    'Lats': {'exercise': exercises.get('back', ['Lat Pulldowns'])[1] if len(exercises.get('back', [])) > 1 else exercises.get('back', ['Rows'])[0], 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                    'Biceps': {'exercise': exercises.get('arms', ['Curls'])[0], 'sets': 3, 'reps': '8-12', 'rest': '60s'},
                },
                'Day 3 (Legs)': {
                    'Quads': {'exercise': exercises.get('legs', ['Squats'])[0], 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    'Hamstrings': {'exercise': exercises.get('legs', ['Deadlifts'])[1] if len(exercises.get('legs', [])) > 1 else exercises.get('legs', ['Squats'])[0], 'sets': 3, 'reps': '8-10', 'rest': '90s'},
                    'Calves': {'exercise': 'Calf Raises', 'sets': 3, 'reps': '12-15', 'rest': '45s'},
                },
                'Day 4 (Push)': {
                    'Chest': {'exercise': exercises.get('chest', ['Push-ups'])[1] if len(exercises.get('chest', [])) > 1 else exercises.get('chest', ['Push-ups'])[0], 'sets': 3, 'reps': '10-12', 'rest': '75s'},
                    'Front Delts': {'exercise': exercises.get('shoulders', [])[1] if len(exercises.get('shoulders', [])) > 1 else exercises.get('shoulders', [])[0], 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                },
                'Day 5 (Pull)': {
                    'Back': {'exercise': exercises.get('back', [])[1] if len(exercises.get('back', [])) > 1 else exercises.get('back', ['Rows'])[0], 'sets': 3, 'reps': '10-12', 'rest': '75s'},
                    'Biceps': {'exercise': exercises.get('arms', [])[1] if len(exercises.get('arms', [])) > 1 else exercises.get('arms', [])[0], 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                },
                'Day 6 (Legs or Cardio)': {
                    'Light Legs': {'exercise': exercises.get('legs', ['Squats'])[2] if len(exercises.get('legs', [])) > 2 else exercises.get('legs', ['Squats'])[0], 'sets': 2, 'reps': '12-15', 'rest': '60s'},
                },
                'Day 7 (Rest)': {'Rest': {'note': 'Complete rest or light stretching', 'sets': 0, 'reps': 'N/A', 'rest': 'N/A'}}
            }
        else:
            # Home-based full body routine
            plan = {
                'Day 1 (Full Body)': {
                    'Chest': {'exercise': 'Push-ups', 'sets': 3, 'reps': '10-15', 'rest': '60s'},
                    'Back': {'exercise': 'Resistance Band Rows', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                    'Legs': {'exercise': 'Bodyweight Squats', 'sets': 3, 'reps': '15-20', 'rest': '60s'},
                },
                'Day 2 (Rest or Light Cardio)': {'Cardio': {'exercise': 'Walking/Jogging', 'sets': 1, 'reps': '30 mins', 'rest': 'N/A'}},
                'Day 3 (Full Body)': {
                    'Chest': {'exercise': 'Diamond Push-ups', 'sets': 3, 'reps': '8-12', 'rest': '60s'},
                    'Legs': {'exercise': 'Lunges', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                    'Cardio': {'exercise': 'Jumping Jacks', 'sets': 3, 'reps': '20 reps', 'rest': '45s'},
                },
                'Day 4 (Rest)': {'Rest': {'note': 'Complete rest', 'sets': 0, 'reps': 'N/A', 'rest': 'N/A'}},
                'Day 5 (Full Body)': {
                    'Back': {'exercise': 'Reverse Snow Angels', 'sets': 3, 'reps': '15-20', 'rest': '60s'},
                    'Arms': {'exercise': 'Tricep Dips', 'sets': 3, 'reps': '8-12', 'rest': '60s'},
                    'Core': {'exercise': 'Planks', 'sets': 3, 'reps': '30-60s', 'rest': '60s'},
                },
                'Day 6 (Cardio/HIIT)': {'Cardio': {'exercise': 'Burpees + High Knees', 'sets': 3, 'reps': '20 reps each', 'rest': '90s'}},
                'Day 7 (Rest)': {'Rest': {'note': 'Complete rest or stretching', 'sets': 0, 'reps': 'N/A', 'rest': 'N/A'}}
            }

        # Adjust volume based on goal
        if goal == 'fat_loss':
            for day in plan:
                if day != 'Day 7 (Rest)' and 'Cardio' not in day and 'Rest' not in day:
                    for muscle in plan[day]:
                        if 'sets' in plan[day][muscle]:
                            plan[day][muscle]['sets'] = max(2, plan[day][muscle]['sets'] - 1)
                            plan[day][muscle]['reps'] = plan[day][muscle]['reps'].replace('8-10', '10-12').replace('10-12', '12-15')

        return plan


class DietPlanGenerator:
    """Generate personalized diet plans"""

    INDIAN_FOOD_DATABASE = {
        'protein_sources': {
            'veg': {
                'paneer': {'protein': 25, 'calories': 265, 'cost': 40, 'quantity': '100g'},
                'tofu': {'protein': 15, 'calories': 76, 'cost': 30, 'quantity': '100g'},
                'soya chunks': {'protein': 50, 'calories': 345, 'cost': 20, 'quantity': '100g'},
                'moong dal': {'protein': 25, 'calories': 347, 'cost': 15, 'quantity': '100g'},
                'chickpeas': {'protein': 19, 'calories': 364, 'cost': 20, 'quantity': '100g'},
                'peanuts': {'protein': 26, 'calories': 567, 'cost': 25, 'quantity': '100g'},
                'milk': {'protein': 3.2, 'calories': 61, 'cost': 5, 'quantity': '100ml'},
                'curd': {'protein': 3.5, 'calories': 60, 'cost': 8, 'quantity': '100g'},
                'eggs': {'protein': 13, 'calories': 155, 'cost': 5, 'quantity': '1 egg'},
            },
            'non_veg': {
                'chicken breast': {'protein': 31, 'calories': 165, 'cost': 100, 'quantity': '100g'},
                'chicken eggs': {'protein': 13, 'calories': 155, 'cost': 5, 'quantity': '1 egg'},
                'fish': {'protein': 26, 'calories': 100, 'cost': 120, 'quantity': '100g'},
                'milk': {'protein': 3.2, 'calories': 61, 'cost': 5, 'quantity': '100ml'},
                'yogurt': {'protein': 3.5, 'calories': 60, 'cost': 8, 'quantity': '100g'},
                'paneer': {'protein': 25, 'calories': 265, 'cost': 40, 'quantity': '100g'},
            }
        },
        'carbs': {
            'rice': {'carbs': 28, 'calories': 130, 'cost': 5, 'quantity': '100g'},
            'roti': {'carbs': 42, 'calories': 200, 'cost': 2, 'quantity': '1 roti'},
            'bread': {'carbs': 49, 'calories': 265, 'cost': 3, 'quantity': '100g'},
            'oats': {'carbs': 66, 'calories': 389, 'cost': 20, 'quantity': '100g'},
            'sweet potato': {'carbs': 20, 'calories': 86, 'cost': 10, 'quantity': '100g'},
            'banana': {'carbs': 27, 'calories': 89, 'cost': 3, 'quantity': '1 banana'},
        },
        'fats': {
            'olive oil': {'fat': 14, 'calories': 119, 'cost': 50, 'quantity': '1 tbsp'},
            'coconut oil': {'fat': 14, 'calories': 119, 'cost': 40, 'quantity': '1 tbsp'},
            'almonds': {'fat': 14, 'calories': 161, 'cost': 30, 'quantity': '23 almonds'},
            'avocado': {'fat': 10, 'calories': 80, 'cost': 50, 'quantity': '100g'},
        },
        'vegetables': {
            'spinach': {'calories': 23, 'cost': 10, 'quantity': '100g'},
            'broccoli': {'calories': 34, 'cost': 15, 'quantity': '100g'},
            'carrot': {'calories': 41, 'cost': 5, 'quantity': '100g'},
            'tomato': {'calories': 18, 'cost': 5, 'quantity': '100g'},
            'onion': {'calories': 40, 'cost': 3, 'quantity': '100g'},
        }
    }

    def generate_plan(self, daily_calories, protein_needed, budget, diet_preference='veg'):
        """
        Generate a daily diet plan

        Args:
            daily_calories: Target daily calories
            protein_needed: Target protein in grams
            budget: Daily budget in INR
            diet_preference: 'veg' or 'non_veg'

        Returns:
            dict with meal suggestions
        """
        protein_sources = self.INDIAN_FOOD_DATABASE['protein_sources'][diet_preference]

        # Allocate macros (rough splits)
        protein_cals = protein_needed * 4  # 4 cal per gram
        carbs_cals = daily_calories * 0.40
        fat_cals = daily_calories * 0.25
        remaining_cals = daily_calories - protein_cals - carbs_cals - fat_cals

        plan = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': [],
            'total_calories': 0,
            'total_protein': 0,
            'total_cost': 0
        }

        # Breakfast: Simple and quick
        breakfast_items = [
            {'item': 'Oats', 'quantity': '50g', 'calories': 195, 'protein': 8, 'cost': 10},
            {'item': 'Milk', 'quantity': '200ml', 'calories': 122, 'protein': 6.4, 'cost': 10},
            {'item': 'Banana', 'quantity': '1', 'calories': 89, 'protein': 1, 'cost': 3}
        ]
        plan['breakfast'] = breakfast_items
        plan['total_calories'] += sum([i['calories'] for i in breakfast_items])
        plan['total_protein'] += sum([i['protein'] for i in breakfast_items])
        plan['total_cost'] += sum([i['cost'] for i in breakfast_items])

        # Lunch: Main meal with protein
        lunch_items = []
        if budget >= 100:
            lunch_items.append({'item': 'Chicken Breast', 'quantity': '150g', 'calories': 248, 'protein': 46.5, 'cost': 150})
        elif diet_preference == 'veg' and budget >= 80:
            lunch_items.append({'item': 'Paneer', 'quantity': '100g', 'calories': 265, 'protein': 25, 'cost': 40})
            lunch_items.append({'item': 'Soya Chunks', 'quantity': '50g', 'calories': 173, 'protein': 25, 'cost': 10})
        else:
            lunch_items.append({'item': 'Moong Dal', 'quantity': '100g', 'calories': 347, 'protein': 25, 'cost': 15})

        lunch_items.extend([
            {'item': 'Rice', 'quantity': '150g', 'calories': 195, 'protein': 4, 'cost': 7},
            {'item': 'Broccoli', 'quantity': '100g', 'calories': 34, 'protein': 2.8, 'cost': 15}
        ])
        plan['lunch'] = lunch_items
        plan['total_calories'] += sum([i['calories'] for i in lunch_items])
        plan['total_protein'] += sum([i['protein'] for i in lunch_items])
        plan['total_cost'] += sum([i['cost'] for i in lunch_items])

        # Dinner: Lighter than lunch
        dinner_items = [
            {'item': 'Roti', 'quantity': '2', 'calories': 400, 'protein': 12, 'cost': 4},
            {'item': 'Curd', 'quantity': '200g', 'calories': 120, 'protein': 7, 'cost': 16},
            {'item': 'Spinach Sabzi', 'quantity': '150g', 'calories': 40, 'protein': 3, 'cost': 10}
        ]
        plan['dinner'] = dinner_items
        plan['total_calories'] += sum([i['calories'] for i in dinner_items])
        plan['total_protein'] += sum([i['protein'] for i in dinner_items])
        plan['total_cost'] += sum([i['cost'] for i in dinner_items])

        # Snacks: Budget dependent
        snacks_items = []
        if plan['total_cost'] < budget:
            remaining_budget = budget - plan['total_cost']
            remaining_calories = daily_calories - plan['total_calories']

            if remaining_budget >= 30:
                snacks_items = [
                    {'item': 'Peanuts', 'quantity': '30g', 'calories': 170, 'protein': 8, 'cost': 7},
                    {'item': 'Apple', 'quantity': '1', 'calories': 95, 'protein': 0.5, 'cost': 8}
                ]
            else:
                snacks_items = [
                    {'item': 'Banana', 'quantity': '1', 'calories': 89, 'protein': 1, 'cost': 3}
                ]

        plan['snacks'] = snacks_items
        plan['total_calories'] += sum([i['calories'] for i in snacks_items])
        plan['total_protein'] += sum([i['protein'] for i in snacks_items])
        plan['total_cost'] += sum([i['cost'] for i in snacks_items])

        return plan


class AIRecommendationEngine:
    """Generate intelligent recommendations based on progress"""

    @staticmethod
    def get_suggestions(current_weight, initial_weight, goal, weeks_elapsed, current_calories):
        """
        Generate AI suggestions based on progress

        Args:
            current_weight: Current user weight
            initial_weight: Starting weight
            goal: 'fat_loss', 'muscle_gain', 'maintenance'
            weeks_elapsed: Number of weeks since start
            current_calories: Current daily calorie intake

        Returns:
            list of suggestions
        """
        suggestions = []
        weight_change = initial_weight - current_weight
        expected_weekly_loss = 0.5  # kg per week for fat loss

        if goal == 'fat_loss':
            if weeks_elapsed > 0:
                actual_weekly_loss = weight_change / weeks_elapsed
                if actual_weekly_loss < expected_weekly_loss * 0.8:
                    suggestions.append({
                        'type': 'calorie_reduction',
                        'message': 'Your weight loss is slower than expected. Consider reducing calories by 200-300 calories.',
                        'action': f'Reduce daily calories to {int(current_calories - 250)}'
                    })
                elif actual_weekly_loss > expected_weekly_loss * 1.5:
                    suggestions.append({
                        'type': 'calorie_increase',
                        'message': 'Your weight loss is too aggressive. Increase calories to preserve muscle.',
                        'action': f'Increase daily calories to {int(current_calories + 150)}'
                    })

            if weeks_elapsed > 8:
                suggestions.append({
                    'type': 'add_cardio',
                    'message': 'Consider adding 2-3 sessions of light cardio (20-30 mins) to break through plateaus.',
                    'action': 'Add walking, cycling, or light running'
                })

        elif goal == 'muscle_gain':
            if weeks_elapsed > 4 and weight_change < 0:
                suggestions.append({
                    'type': 'increase_calories',
                    'message': 'You need to be in a calorie surplus for muscle gain. Increase calories by 300-500.',
                    'action': f'Increase daily calories to {int(current_calories + 400)}'
                })

        elif goal == 'maintenance':
            if abs(weight_change) > 2:
                suggestions.append({
                    'type': 'stabilize_diet',
                    'message': 'Your weight is fluctuating. Try to keep calories consistent.',
                    'action': f'Maintain daily calories at {int(current_calories)}'
                })

        return suggestions
