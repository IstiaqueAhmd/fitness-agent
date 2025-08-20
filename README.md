# Agentic Fitness Chatbot

An intelligent fitness assistant powered by OpenAI's function calling capabilities that can generate personalized fitness plans and store them for users.

## Features

### 🤖 Agentic AI Capabilities
- **Workout Plan Generation**: Creates personalized workout plans based on user goals, fitness level, and available time
- **Nutrition Plan Creation**: Generates custom nutrition plans with macro calculations
- **Plan Storage**: Automatically saves fitness plans when requested by users
- **Plan Retrieval**: Retrieves previously saved plans for users

### 🛠️ Tool Functions
The chatbot has access to the following tools:

1. **`generate_workout_plan`**: Creates comprehensive workout plans
   - Parameters: goals, fitness_level, available_days, duration_weeks, equipment
   
2. **`generate_nutrition_plan`**: Generates nutrition plans with macro calculations
   - Parameters: goals, current_weight, target_weight, activity_level, dietary_restrictions
   
3. **`save_fitness_plan`**: Stores generated plans in the database
   - Parameters: user_id, session_id, plan_data, plan_type
   
4. **`get_user_fitness_plans`**: Retrieves all saved plans for a user
   - Parameters: user_id

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fitness-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.template .env
   # Edit .env and add your OpenAI API key
   ```

4. **Initialize the database**
   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

5. **Run the application**
   ```bash
   python -m app.main
   ```

## Usage Examples

### Example 1: Generate and Save a Workout Plan
```
User: "I want to create a workout plan. I'm a beginner, want to lose weight, and can work out 4 days a week with basic equipment at home."

AI: [Generates a comprehensive workout plan with exercises, sets, reps, and schedule]

User: "Please save this workout plan for me."

AI: "I've successfully saved your workout plan! You can retrieve it anytime by asking me to show your saved plans."
```

### Example 2: Create a Nutrition Plan
```
User: "Can you create a nutrition plan for me? I'm 180 pounds, want to lose weight to 160 pounds, and I'm moderately active."

AI: [Generates a detailed nutrition plan with daily calories, macros, and meal suggestions]

User: "Save this nutrition plan too."

AI: "Your nutrition plan has been saved successfully!"
```

### Example 3: Retrieve Saved Plans
```
User: "Show me all my saved fitness plans."

AI: [Lists all previously saved workout and nutrition plans with details]
```

## API Endpoints

### Chat Endpoints
- `POST /chat` - Send messages to the agentic chatbot
- `GET /chat/{session_id}/history` - Get chat history for a session

### Session Management
- `POST /sessions` - Create a new chat session
- `GET /sessions/{user_id}` - Get all sessions for a user
- `DELETE /sessions/{session_id}` - Delete a session

### Fitness Plans
- `GET /fitness-plans/{user_id}` - Get all saved fitness plans for a user

## Architecture

### Key Components

1. **`chat.py`** - Main chatbot class with tool calling capabilities
2. **`tools.py`** - Fitness-specific tool functions
3. **`database.py`** - Database models and connection
4. **`agent.py`** - OpenAI function calling implementation
5. **`main.py`** - FastAPI application with endpoints

### Database Schema

- **ChatSession**: Stores chat sessions
- **ChatMessage**: Stores individual messages
- **FitnessPlan**: Stores generated fitness plans with full JSON data

### Tool Calling Flow

1. User sends a message requesting a fitness plan
2. AI determines which tools to use based on the request
3. Tools are called with extracted parameters
4. Results are processed and presented to the user
5. Plans can be saved to the database when requested

## Testing

Run the test script to see the agentic functionality in action:

```bash
python test_agent.py
```

This script demonstrates:
- Generating workout plans
- Generating nutrition plans  
- Saving plans to the database
- Retrieving saved plans

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

### Supported Parameters

#### Workout Plans
- **Fitness Levels**: beginner, intermediate, advanced
- **Goals**: weight loss, muscle gain, general fitness
- **Equipment**: basic, gym, home, none
- **Duration**: 4-24 weeks

#### Nutrition Plans
- **Activity Levels**: sedentary, light, moderate, active, very_active
- **Goals**: weight loss, weight gain, maintenance
- **Dietary Restrictions**: Custom text field

## Advanced Features

### Tool Calling Intelligence
The AI automatically determines when to use tools based on user requests. It can:
- Extract parameters from natural language
- Chain multiple tool calls together
- Handle errors gracefully
- Provide contextual responses

### Data Persistence
All generated plans are stored with:
- Full plan details in JSON format
- User and session association
- Timestamps for tracking
- Plan type categorization

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.