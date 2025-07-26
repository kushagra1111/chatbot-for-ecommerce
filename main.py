# main.py

from fastapi import FastAPI, HTTPException, Depends  # Import FastAPI and dependencies
from pydantic import BaseModel  # Import BaseModel for request validation
from sqlalchemy import create_engine  # Import create_engine for DB connection
from sqlalchemy.orm import sessionmaker, Session  # Import sessionmaker and Session
from datetime import datetime  # Import datetime for timestamps

# Import your models (make sure models.py is in the same directory)
from models import User, Session as ChatSession, Message, Base  # Import models

DATABASE_URL = "sqlite:///./test.db"  # Set your database URL

engine = create_engine(DATABASE_URL)  # Create database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Create session factory

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)  # Create all tables

app = FastAPI()  # Initialize FastAPI app

# Dependency to get DB session
def get_db():
    db = SessionLocal()  # Create DB session
    try:
        yield db  # Yield DB session
    finally:
        db.close()  # Close DB session

# Request schema
class ChatRequest(BaseModel):
    user_id: int  # User ID
    message: str  # User message
    conversation_id: int = None  # Optional conversation/session ID

# Response schema
class ChatResponse(BaseModel):
    conversation_id: int  # Conversation/session ID
    user_message: str  # User message
    ai_message: str  # AI response

# Dummy AI response function (replace with real AI logic)
def get_ai_response(user_message: str) -> str:
    return f"AI response to: {user_message}"  # Return dummy response

@app.post("/ask")
async def ask_agent(request: Request):  # Define POST endpoint
    data = await request.json()  # Parse incoming JSON request
    user_message = data.get("message")  # Extract user message

    # Step 1: Send user message to LLM for processing
    llm_response = openai.ChatCompletion.create(
        model="llama2-70b-4096",  # Use Groq-supported model
        messages=[{"role": "user", "content": user_message}]  # Pass user message
    )  # Get LLM response

    agent_reply = llm_response['choices'][0]['message']['content']  # Extract LLM reply

    # Step 2: Query the database (example query)
    with engine.connect() as conn:  # Connect to database
        result = conn.execute(text("SELECT * FROM users LIMIT 1"))  # Example SQL query, table 'users'
        db_data = [dict(row) for row in result]  # Convert result to list of dicts

    # Step 3: Return combined response
    return {
        "agent_reply": agent_reply,  # LLM's response
        "db_data": db_data  # Database query result
    }
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == request.user_id).first()  # Query user
    if not user:  # If user not found
        raise HTTPException(status_code=404, detail="User not found")  # Raise error

    # Handle session/conversation
    if request.conversation_id:  # If conversation_id provided
        session_obj = db.query(ChatSession).filter(ChatSession.id == request.conversation_id).first()  # Query session
        if not session_obj:  # If session not found
            raise HTTPException(status_code=404, detail="Conversation not found")  # Raise error
    else:  # If no conversation_id, create new session
        session_obj = ChatSession(user_id=user.id, started_at=datetime.utcnow())  # Create new session
        db.add(session_obj)  # Add to DB
        db.commit()  # Commit to get ID
        db.refresh(session_obj)  # Refresh to get new ID

    # Save user message
    user_msg = Message(
        session_id=session_obj.id,  # Link to session
        sender="user",  # Sender is user
        message_text=request.message,  # User message
        timestamp=datetime.utcnow()  # Current time
    )
    db.add(user_msg)  # Add to DB

    # Generate AI response
    ai_response = get_ai_response(request.message)  # Get AI response

    # Save AI message
    ai_msg = Message(
        session_id=session_obj.id,  # Link to session
        sender="ai",  # Sender is AI
        message_text=ai_response,  # AI response
        timestamp=datetime.utcnow()  # Current time
    )
    db.add(ai_msg)  # Add to DB

    db.commit()  # Commit both messages

    return ChatResponse(
        conversation_id=session_obj.id,  # Return session ID
        user_message=request.message,  # Return user message
        ai_message=ai_response  # Return AI response
    )
