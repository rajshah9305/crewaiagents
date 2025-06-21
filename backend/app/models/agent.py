from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    goal = Column(Text, nullable=False)
    backstory = Column(Text, nullable=False)
    
    # CrewAI specific fields
    tools = Column(JSON, default=list)  # List of tool names
    llm_config = Column(JSON, default=dict)  # Cerebras model config
    memory_enabled = Column(Boolean, default=True)
    allow_delegation = Column(Boolean, default=False)
    verbose = Column(Boolean, default=True)
    
    # Performance tracking
    total_executions = Column(Integer, default=0)
    success_rate = Column(Integer, default=0)
    avg_response_time = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="agents")
    team_agents = relationship("TeamAgent", back_populates="agent")
    messages = relationship("Message", back_populates="agent")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    process_type = Column(String(50), default="sequential")  # sequential, hierarchical
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="teams")
    team_agents = relationship("TeamAgent", back_populates="team")
    conversations = relationship("Conversation", back_populates="team")

class TeamAgent(Base):
    __tablename__ = "team_agents"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    order = Column(Integer, default=0)
    is_manager = Column(Boolean, default=False)
    
    # Relationships
    team = relationship("Team", back_populates="team_agents")
    agent = relationship("Agent", back_populates="team_agents") 