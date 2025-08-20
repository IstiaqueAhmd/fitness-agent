from openai import OpenAI
from typing import List, Dict, Any, Optional
import os
import json
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from tools import call_fitness_function

load_dotenv()

class FitnessChat:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """You are an intelligent fitness and health assistant with the ability to create personalized fitness plans. You can:

1. Generate comprehensive workout plans based on user goals, fitness level, and available time
2. Create nutrition plans tailored to weight goals and dietary preferences  
3. Save fitness plans when users request it
4. Retrieve previously saved plans for users

When users ask for fitness plans, use the appropriate tools to generate them. Always ask for necessary details like:
- Fitness goals (weight loss, muscle gain, general fitness)
- Current fitness level (beginner, intermediate, advanced)
- Available workout days per week
- Any equipment limitations
- For nutrition plans: current weight, target weight, activity level, dietary restrictions

Be encouraging and provide evidence-based advice. Always recommend consulting healthcare professionals for serious health concerns.

When a user asks you to save a plan, use the save_fitness_plan function. When they want to see their previous plans, use get_user_fitness_plans.
"""

    def get_fitness_tools(self):
        """Define the available fitness tools for the AI agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "generate_workout_plan",
                    "description": "Generate a comprehensive workout plan based on user goals and parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_goals": {
                                "type": "string",
                                "description": "User's fitness goals (e.g., weight loss, muscle gain, general fitness)"
                            },
                            "fitness_level": {
                                "type": "string",
                                "enum": ["beginner", "intermediate", "advanced"],
                                "description": "User's current fitness level"
                            },
                            "available_days": {
                                "type": "integer",
                                "description": "Number of days per week available for workouts"
                            },
                            "duration_weeks": {
                                "type": "integer",
                                "description": "Duration of the plan in weeks",
                                "default": 12
                            },
                            "equipment": {
                                "type": "string",
                                "description": "Available equipment (basic, gym, home, none)",
                                "default": "basic"
                            }
                        },
                        "required": ["user_goals", "fitness_level", "available_days"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_nutrition_plan",
                    "description": "Generate a nutrition plan based on user goals and parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_goals": {
                                "type": "string",
                                "description": "User's nutrition/weight goals"
                            },
                            "current_weight": {
                                "type": "number",
                                "description": "User's current weight in pounds or kg"
                            },
                            "target_weight": {
                                "type": "number",
                                "description": "User's target weight in pounds or kg"
                            },
                            "activity_level": {
                                "type": "string",
                                "enum": ["sedentary", "light", "moderate", "active", "very_active"],
                                "description": "User's activity level"
                            },
                            "dietary_restrictions": {
                                "type": "string",
                                "description": "Any dietary restrictions or preferences",
                                "default": "none"
                            }
                        },
                        "required": ["user_goals", "current_weight", "target_weight", "activity_level"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_fitness_plan",
                    "description": "Save a generated fitness plan to the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User's ID"
                            },
                            "session_id": {
                                "type": "string",
                                "description": "Current session ID"
                            },
                            "plan_data": {
                                "type": "object",
                                "description": "The fitness plan data to save"
                            },
                            "plan_type": {
                                "type": "string",
                                "enum": ["workout", "nutrition", "combined"],
                                "description": "Type of fitness plan"
                            }
                        },
                        "required": ["user_id", "session_id", "plan_data", "plan_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_user_fitness_plans",
                    "description": "Retrieve all saved fitness plans for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User's ID"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            }
        ]
    
    def generate_response(self, message: str, conversation_history: List[Dict[str, str]] = None, 
                         user_id: str = "anonymous", session_id: str = None, db_session: Session = None) -> str:
        """Generate a response using OpenAI API with tool calling capabilities"""
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add the current user message
            messages.append({"role": "user", "content": message})
            
            # Get available tools
            tools = self.get_fitness_tools()
            
            # Initial API call with tools
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=1500,
                temperature=0.7
            )
            
            response_message = response.choices[0].message
            
            # Check if the model wants to call any functions
            if response_message.tool_calls:
                # Add the assistant's response to messages
                messages.append(response_message)
                
                # Process each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Add database session and user context for functions that need it
                    if function_name in ["save_fitness_plan", "get_user_fitness_plans"] and db_session:
                        if function_name == "save_fitness_plan":
                            function_args["user_id"] = user_id
                            function_args["session_id"] = session_id
                        elif function_name == "get_user_fitness_plans":
                            function_args["user_id"] = user_id
                    
                    try:
                        # Call the function
                        function_result = call_fitness_function(function_name, function_args, db_session)
                        
                        # Add function result to messages
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(function_result, default=str)
                        })
                    except Exception as e:
                        # Handle function call errors
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": f"Error calling function: {str(e)}"
                        })
                
                # Get final response with function results
                final_response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    tools=tools,
                    max_tokens=1500,
                    temperature=0.7
                )
                
                return final_response.choices[0].message.content
            else:
                # No function calls, return the regular response
                return response_message.content
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."
    
    def get_conversation_context(self, messages: List[Dict[str, str]], max_messages: int = 10) -> List[Dict[str, str]]:
        """Get recent conversation context for API calls"""
        return messages[-max_messages:] if len(messages) > max_messages else messages