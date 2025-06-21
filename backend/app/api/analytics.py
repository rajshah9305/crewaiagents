from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.agent import Agent, Team
from app.models.conversation import Conversation, Message
from typing import Dict, List, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

class DashboardMetrics(BaseModel):
    total_agents: int
    total_teams: int
    total_messages: int
    avg_response_time: int
    avg_success_rate: int
    most_active_agent: Dict[str, Any]
    recent_conversations: List[Dict[str, Any]]

@router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard metrics for a user"""
    
    # Agent metrics
    total_agents = db.query(Agent).filter(
        Agent.user_id == current_user.id,
        Agent.is_active == True
    ).count()
    
    # Most active agent
    most_active_agent = db.query(Agent).filter(
        Agent.user_id == current_user.id,
        Agent.is_active == True
    ).order_by(desc(Agent.total_executions)).first()
    
    # Team metrics
    total_teams = db.query(Team).filter(
        Team.user_id == current_user.id,
        Team.is_active == True
    ).count()
    
    # Recent conversations
    recent_conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(desc(Conversation.created_at)).limit(5).all()
    
    # Usage metrics (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    total_messages = db.query(Message).join(Conversation).filter(
        Conversation.user_id == current_user.id,
        Message.created_at >= thirty_days_ago
    ).count()
    
    # Average response time
    avg_response_time = db.query(func.avg(Agent.avg_response_time)).filter(
        Agent.user_id == current_user.id,
        Agent.is_active == True
    ).scalar() or 0
    
    # Success rate
    avg_success_rate = db.query(func.avg(Agent.success_rate)).filter(
        Agent.user_id == current_user.id,
        Agent.is_active == True
    ).scalar() or 0
    
    return DashboardMetrics(
        total_agents=total_agents,
        total_teams=total_teams,
        total_messages=total_messages,
        avg_response_time=int(avg_response_time),
        avg_success_rate=int(avg_success_rate),
        most_active_agent={
            "name": most_active_agent.name if most_active_agent else None,
            "executions": most_active_agent.total_executions if most_active_agent else 0
        },
        recent_conversations=[
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at
            } for conv in recent_conversations
        ]
    )

@router.get("/performance")
def get_agent_performance_data(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get agent performance data for charts"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    agents = db.query(Agent).filter(
        Agent.user_id == current_user.id,
        Agent.is_active == True,
        Agent.created_at >= cutoff_date
    ).all()
    
    return [
        {
            "name": agent.name,
            "executions": agent.total_executions,
            "success_rate": agent.success_rate,
            "avg_response_time": agent.avg_response_time,
            "created_at": agent.created_at.isoformat()
        } for agent in agents
    ]

@router.get("/trends")
def get_usage_trends(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get usage trends over time"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily message counts
    daily_messages = db.query(
        func.date(Message.created_at).label('date'),
        func.count(Message.id).label('count')
    ).join(Conversation).filter(
        Conversation.user_id == current_user.id,
        Message.created_at >= cutoff_date
    ).group_by(func.date(Message.created_at)).all()
    
    # Agent creation trend
    daily_agents = db.query(
        func.date(Agent.created_at).label('date'),
        func.count(Agent.id).label('count')
    ).filter(
        Agent.user_id == current_user.id,
        Agent.created_at >= cutoff_date
    ).group_by(func.date(Agent.created_at)).all()
    
    return {
        "message_trends": [
            {"date": str(date), "count": count} 
            for date, count in daily_messages
        ],
        "agent_creation_trends": [
            {"date": str(date), "count": count} 
            for date, count in daily_agents
        ]
    } 