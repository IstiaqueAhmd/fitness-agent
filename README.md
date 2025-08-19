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

## Postman API Requests

### 1. Root Endpoint
```http
GET http://127.0.0.1:8000/
```

### 2. Health Check
```http
GET http://127.0.0.1:8000/health
```

### 3. Chat Endpoint
```http
POST http://127.0.0.1:8000/chat
Content-Type: application/json

{
    "user_id": "user123",
    "message": "What's a good workout routine for beginners?",
    "session_id": "optional-session-id"
}
```

### 4. Create Session
```http
POST http://127.0.0.1:8000/sessions?user_id=user123&title=My Workout Chat
```

### 5. Get User Sessions
```http
GET http://127.0.0.1:8000/sessions/user123
```

### 6. Get Chat History
```http
GET http://127.0.0.1:8000/chat/session-id-here/history
```

### 7. Delete Session
```http
DELETE http://127.0.0.1:8000/sessions/session-id-here?user_id=user123
```

### 8. Update Session Title
```http
PUT http://127.0.0.1:8000/sessions/session-id-here/title?title=Updated Chat Title&user_id=user123
```

### Sample Requests

**Chat Request Example:**
```json
{
    "user_id": "user123",
    "message": "I want to lose weight. Can you suggest a workout plan?",
    "session_id": null
}
```

**Create Session Example:**
Query parameters: `user_id=user123&title=Weight Loss Journey`

### Postman Environment Variables
- `base_url`: `http://127.0.0.1:8000`
- `user_id`: `user123`
- `session_id`: `your-session-id`

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