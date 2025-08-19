# Fitness Chat API

A FastAPI-based fitness and health chat application powered by OpenAI's GPT models.

## Features

- 🤖 AI-powered fitness and health advice
- 💬 Chat sessions with conversation history
- 📊 Session management (create, delete, update)
- 🗄️ SQLite database for data persistence
- 🚀 RESTful API endpoints
- 📚 Interactive API documentation

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fitness-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment configuration**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Chat
- `POST /chat` - Send a message and get AI response
- `GET /chat/{session_id}/history` - Get chat history for a session

### Session Management
- `POST /sessions` - Create a new chat session
- `GET /sessions/{user_id}` - Get all sessions for a user
- `DELETE /sessions/{session_id}` - Delete a chat session
- `PUT /sessions/{session_id}/title` - Update session title

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Start a chat conversation
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "I want to start a workout routine for beginners",
       "user_id": "user123"
     }'
```

### Get chat history
```bash
curl "http://localhost:8000/chat/{session_id}/history"
```

### Create a new session
```bash
curl -X POST "http://localhost:8000/sessions?user_id=user123&title=My Workout Plan"
```

## Database

The application uses SQLite by default, storing data in `fitness_chat.db`. The database includes:

- **chat_sessions**: Stores chat session metadata
- **chat_messages**: Stores individual messages in conversations

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

## License

This project is open source and available under the MIT License.