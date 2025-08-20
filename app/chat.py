from openai import OpenAI
from typing import List, Dict
import os
import json
from dotenv import load_dotenv
from tools import call_function

load_dotenv()

class FitnessChat:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """You are FitBot, an expert fitness coach and personal trainer assistant. You help users create personalized workout plans, provide fitness advice, and can save workout plans when requested. 

Your capabilities include:
- Creating customized workout plans based on user goals, fitness level, and preferences
- Providing exercise instructions and form tips
- Suggesting nutrition advice
- Saving workout plans to the user's profile when they ask you to save them
- Retrieving previously saved workout plans

When creating workout plans, be specific and include:
- Exercise names
- Sets and reps
- Rest periods
- Progression tips
- Safety considerations

If a user asks you to save a workout plan, use the save_workout_plan function. Always ask for a plan name if not provided."""
    
    def generate_response(self, message: str, conversation_history: List[Dict[str, str]] = None, user_id: str = "anonymous", session_id: str = None) -> str:
        """Generate a response using OpenAI API with tool calling capabilities"""
        try:
            # Define available tools
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "save_workout_plan",
                        "description": "Save a workout plan to the user's profile in the database",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {
                                    "type": "string",
                                    "description": "The user's ID"
                                },
                                "plan_name": {
                                    "type": "string",
                                    "description": "A descriptive name for the workout plan"
                                },
                                "plan_content": {
                                    "type": "string",
                                    "description": "The detailed workout plan content including exercises, sets, reps, etc."
                                },
                                "session_id": {
                                    "type": "string",
                                    "description": "The current chat session ID"
                                }
                            },
                            "required": ["user_id", "plan_name", "plan_content"],
                            "additionalProperties": False
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_user_workout_plans",
                        "description": "Retrieve all saved workout plans for a user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {
                                    "type": "string",
                                    "description": "The user's ID"
                                }
                            },
                            "required": ["user_id"],
                            "additionalProperties": False
                        }
                    }
                }
            ]

            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add the current user message
            messages.append({"role": "user", "content": message})
            
            # First API call to determine if tools are needed
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=1000,
                temperature=0.7
            )
            
            response_message = response.choices[0].message
            
            # Check if the model wants to call a function
            if response_message.tool_calls:
                # Add the assistant's response to messages
                messages.append(response_message)
                
                # Execute each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Add user_id and session_id to function args if not present
                    if "user_id" in function_args and function_args["user_id"] == "":
                        function_args["user_id"] = user_id
                    if "session_id" not in function_args and session_id:
                        function_args["session_id"] = session_id
                    
                    # Call the function
                    function_result = call_function(function_name, function_args)
                    
                    # Add the function result to messages
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_result)
                    })
                
                # Get the final response from the model
                final_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                return final_response.choices[0].message.content
            else:
                # No tool calls needed, return the response directly
                return response_message.content
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."
    
    def get_conversation_context(self, messages: List[Dict[str, str]], max_messages: int = 10) -> List[Dict[str, str]]:
        """Get recent conversation context for API calls"""
        return messages[-max_messages:] if len(messages) > max_messages else messages