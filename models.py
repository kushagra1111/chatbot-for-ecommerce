
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime  # Import SQLAlchemy column types
from sqlalchemy.orm import relationship, declarative_base  # Import relationship and base class
from datetime import datetime  # Import datetime for timestamps

Base = declarative_base()  # Create base class for models

class User(Base):  # Define User model
    __tablename__ = "users"  # Table name
    id = Column(Integer, primary_key=True, index=True)  # User ID, primary key
    name = Column(String(100))  # User name
    email = Column(String(100), unique=True, index=True)  # User email, unique

    sessions = relationship("Session", back_populates="user")  # Relationship to sessions

class Session(Base):  # Define Session model
    __tablename__ = "sessions"  # Table name
    id = Column(Integer, primary_key=True, index=True)  # Session ID, primary key
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to users
    started_at = Column(DateTime, default=datetime.utcnow)  # Session start time
    ended_at = Column(DateTime, nullable=True)  # Session end time, nullable

    user = relationship("User", back_populates="sessions")  # Relationship to user
    messages = relationship("Message", back_populates="session")  # Relationship to messages

class Message(Base):  # Define Message model
    __tablename__ = "messages"  # Table name
    id = Column(Integer, primary_key=True, index=True)  # Message ID, primary key
    session_id = Column(Integer, ForeignKey("sessions.id"))  # Foreign key to sessions
    sender = Column(String(10))  # 'user' or 'ai'
    message_text = Column(Text)  # Message content
    timestamp = Column(DateTime, default=datetime.utcnow)  # Message timestamp

    session = relationship("Session", back_populates="messages")  # Relationship to session
