from sqlalchemy.orm import Session
from database import SessionLocal, WorkoutPlan
from datetime import datetime
import json


def save_workout_plan(user_id: str, plan_name: str, plan_content: str, session_id: str = None) -> dict:
    """
    Save a workout plan to the database
    
    Args:
        user_id: The ID of the user
        plan_name: Name/title of the workout plan
        plan_content: The detailed workout plan content
        session_id: Optional session ID for tracking
    
    Returns:
        dict: Success message with plan ID
    """
    try:
        db = SessionLocal()
        
        workout_plan = WorkoutPlan(
            user_id=user_id,
            plan_name=plan_name,
            plan_content=plan_content,
            session_id=session_id,
            created_at=datetime.utcnow()
        )
        
        db.add(workout_plan)
        db.commit()
        db.refresh(workout_plan)
        db.close()
        
        return {
            "success": True,
            "message": f"Workout plan '{plan_name}' saved successfully!",
            "plan_id": workout_plan.id
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error saving workout plan: {str(e)}"
        }


def get_user_workout_plans(user_id: str) -> dict:
    """
    Retrieve all workout plans for a specific user
    
    Args:
        user_id: The ID of the user
    
    Returns:
        dict: List of workout plans
    """
    try:
        db = SessionLocal()
        
        plans = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).all()
        db.close()
        
        plan_list = []
        for plan in plans:
            plan_list.append({
                "id": plan.id,
                "plan_name": plan.plan_name,
                "plan_content": plan.plan_content,
                "created_at": plan.created_at.isoformat(),
                "session_id": plan.session_id
            })
        
        return {
            "success": True,
            "plans": plan_list,
            "count": len(plan_list)
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving workout plans: {str(e)}"
        }


def call_function(name: str, args: dict):
    """Execute the appropriate function based on name"""
    if name == "save_workout_plan":
        return save_workout_plan(**args)
    elif name == "get_user_workout_plans":
        return get_user_workout_plans(**args)
    else:
        raise ValueError(f"Unknown function: {name}")