"""
Fitness Agent Tools
This module contains tools for generating and managing fitness plans.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .database import FitnessPlan, get_db


def generate_workout_plan(
    user_goals: str,
    fitness_level: str,
    available_days: int,
    duration_weeks: int = 12,
    equipment: str = "basic"
) -> Dict[str, Any]:
    """
    Generate a comprehensive workout plan based on user parameters.
    """
    
    # Define workout templates based on fitness level and goals
    workout_templates = {
        "beginner": {
            "weight_loss": {
                "structure": "3-day full body",
                "exercises_per_day": 6,
                "sets": "2-3",
                "reps": "12-15",
                "rest": "60-90 seconds"
            },
            "muscle_gain": {
                "structure": "3-day full body",
                "exercises_per_day": 7,
                "sets": "3-4",
                "reps": "8-12",
                "rest": "90-120 seconds"
            },
            "general_fitness": {
                "structure": "3-day full body",
                "exercises_per_day": 6,
                "sets": "2-3",
                "reps": "10-15",
                "rest": "60-90 seconds"
            }
        },
        "intermediate": {
            "weight_loss": {
                "structure": "4-day upper/lower split",
                "exercises_per_day": 7,
                "sets": "3-4",
                "reps": "10-15",
                "rest": "60-90 seconds"
            },
            "muscle_gain": {
                "structure": "4-day push/pull/legs",
                "exercises_per_day": 8,
                "sets": "3-4",
                "reps": "6-12",
                "rest": "90-120 seconds"
            }
        },
        "advanced": {
            "weight_loss": {
                "structure": "5-6 day split",
                "exercises_per_day": 8,
                "sets": "4-5",
                "reps": "8-15",
                "rest": "45-90 seconds"
            },
            "muscle_gain": {
                "structure": "5-6 day body part split",
                "exercises_per_day": 9,
                "sets": "4-5",
                "reps": "6-12",
                "rest": "90-120 seconds"
            }
        }
    }
    
    # Determine plan type based on goals
    plan_type = "general_fitness"
    if "weight loss" in user_goals.lower() or "lose weight" in user_goals.lower():
        plan_type = "weight_loss"
    elif "muscle" in user_goals.lower() or "gain" in user_goals.lower() or "bulk" in user_goals.lower():
        plan_type = "muscle_gain"
    
    # Get template
    template = workout_templates.get(fitness_level, workout_templates["beginner"]).get(plan_type, workout_templates["beginner"]["general_fitness"])
    
    # Generate weekly schedule
    weekly_schedule = {}
    
    if available_days >= 3:
        if plan_type == "weight_loss":
            weekly_schedule = {
                "Day 1": "Full Body Strength + 20min Cardio",
                "Day 2": "Rest or Light Walking",
                "Day 3": "Full Body Strength + 15min HIIT",
                "Day 4": "Rest or Yoga",
                "Day 5": "Full Body Strength + 20min Cardio",
                "Day 6": "Active Recovery",
                "Day 7": "Rest"
            }
        elif plan_type == "muscle_gain":
            weekly_schedule = {
                "Day 1": "Upper Body (Push)",
                "Day 2": "Lower Body",
                "Day 3": "Rest",
                "Day 4": "Upper Body (Pull)",
                "Day 5": "Full Body",
                "Day 6": "Rest",
                "Day 7": "Rest"
            }
        else:
            weekly_schedule = {
                "Day 1": "Full Body Workout",
                "Day 2": "Rest or Light Activity",
                "Day 3": "Full Body Workout",
                "Day 4": "Rest",
                "Day 5": "Full Body Workout",
                "Day 6": "Active Recovery",
                "Day 7": "Rest"
            }
    
    workout_plan = {
        "plan_name": f"{fitness_level.title()} {plan_type.replace('_', ' ').title()} Plan",
        "goals": user_goals,
        "fitness_level": fitness_level,
        "duration_weeks": duration_weeks,
        "available_days": available_days,
        "equipment_needed": equipment,
        "structure": template["structure"],
        "weekly_schedule": weekly_schedule,
        "exercise_parameters": {
            "sets": template["sets"],
            "reps": template["reps"],
            "rest_periods": template["rest"],
            "exercises_per_session": template["exercises_per_day"]
        },
        "progression_notes": "Increase weight by 2.5-5lbs when you can complete all sets with good form",
        "created_at": datetime.utcnow().isoformat()
    }
    
    return workout_plan


def generate_nutrition_plan(
    user_goals: str,
    current_weight: float,
    target_weight: float,
    activity_level: str,
    dietary_restrictions: str = "none"
) -> Dict[str, Any]:
    """
    Generate a nutrition plan based on user parameters.
    """
    
    # Calculate approximate daily calories based on activity level and goals
    base_calories = current_weight * 10  # Very rough estimate
    
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.375)
    maintenance_calories = int(base_calories * multiplier)
    
    # Adjust calories based on goals
    if "weight loss" in user_goals.lower() or target_weight < current_weight:
        daily_calories = maintenance_calories - 500  # 1lb/week loss
        goal_type = "weight_loss"
    elif "gain" in user_goals.lower() or target_weight > current_weight:
        daily_calories = maintenance_calories + 300  # Lean gain
        goal_type = "weight_gain"
    else:
        daily_calories = maintenance_calories
        goal_type = "maintenance"
    
    # Macronutrient distribution
    if goal_type == "weight_loss":
        protein_ratio = 0.35
        carb_ratio = 0.35
        fat_ratio = 0.30
    elif goal_type == "weight_gain":
        protein_ratio = 0.25
        carb_ratio = 0.45
        fat_ratio = 0.30
    else:
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
    
    protein_calories = daily_calories * protein_ratio
    carb_calories = daily_calories * carb_ratio
    fat_calories = daily_calories * fat_ratio
    
    protein_grams = int(protein_calories / 4)
    carb_grams = int(carb_calories / 4)
    fat_grams = int(fat_calories / 9)
    
    nutrition_plan = {
        "plan_name": f"{goal_type.replace('_', ' ').title()} Nutrition Plan",
        "goals": user_goals,
        "current_weight": current_weight,
        "target_weight": target_weight,
        "daily_calories": daily_calories,
        "macronutrients": {
            "protein": f"{protein_grams}g",
            "carbohydrates": f"{carb_grams}g",
            "fats": f"{fat_grams}g"
        },
        "meal_timing": {
            "breakfast": "25% of daily calories",
            "lunch": "30% of daily calories",
            "dinner": "30% of daily calories",
            "snacks": "15% of daily calories"
        },
        "food_suggestions": {
            "proteins": ["Chicken breast", "Fish", "Eggs", "Greek yogurt", "Lean beef", "Tofu"],
            "carbohydrates": ["Oats", "Brown rice", "Sweet potatoes", "Quinoa", "Fruits", "Vegetables"],
            "fats": ["Avocado", "Nuts", "Olive oil", "Fatty fish", "Seeds"]
        },
        "hydration": "Aim for 8-10 glasses of water daily",
        "dietary_restrictions": dietary_restrictions,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return nutrition_plan


def save_fitness_plan(
    db: Session,
    user_id: str,
    session_id: str,
    plan_data: Dict[str, Any],
    plan_type: str
) -> int:
    """
    Save a fitness plan to the database.
    """
    
    fitness_plan = FitnessPlan(
        user_id=user_id,
        session_id=session_id,
        plan_name=plan_data.get("plan_name", "Custom Plan"),
        plan_type=plan_type,
        plan_data=plan_data,
        goals=plan_data.get("goals", ""),
        duration_weeks=plan_data.get("duration_weeks", 12),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(fitness_plan)
    db.commit()
    db.refresh(fitness_plan)
    
    return fitness_plan.id


def get_user_fitness_plans(db: Session, user_id: str) -> list:
    """
    Retrieve all fitness plans for a user.
    """
    plans = db.query(FitnessPlan).filter(FitnessPlan.user_id == user_id).all()
    return [
        {
            "id": plan.id,
            "plan_name": plan.plan_name,
            "plan_type": plan.plan_type,
            "goals": plan.goals,
            "duration_weeks": plan.duration_weeks,
            "created_at": plan.created_at.isoformat(),
            "plan_data": plan.plan_data
        }
        for plan in plans
    ]


def call_fitness_function(name: str, args: Dict[str, Any], db_session: Session = None) -> Any:
    """
    Route function calls to the appropriate fitness function.
    """
    if name == "generate_workout_plan":
        return generate_workout_plan(**args)
    elif name == "generate_nutrition_plan":
        return generate_nutrition_plan(**args)
    elif name == "save_fitness_plan" and db_session:
        return save_fitness_plan(db_session, **args)
    elif name == "get_user_fitness_plans" and db_session:
        return get_user_fitness_plans(db_session, **args)
    else:
        raise ValueError(f"Unknown function: {name}")