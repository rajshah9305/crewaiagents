from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.agent import Team, TeamAgent, Agent
from app.services.agent_service import AgentService
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate, TeamAgentAdd, TeamExecutionRequest

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new team"""
    team = Team(
        user_id=current_user.id,
        name=team_data.name,
        description=team_data.description,
        process_type=team_data.process_type
    )
    
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

@router.get("/", response_model=List[TeamResponse])
def get_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's teams"""
    teams = db.query(Team).filter(
        Team.user_id == current_user.id,
        Team.is_active == True
    ).all()
    return teams

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific team with agents"""
    team = db.query(Team).filter(
        Team.id == team_id,
        Team.user_id == current_user.id
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/{team_id}/agents")
def add_agent_to_team(
    team_id: int,
    agent_data: TeamAgentAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add agent to team"""
    # Verify team ownership
    team = db.query(Team).filter(
        Team.id == team_id,
        Team.user_id == current_user.id
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Verify agent ownership
    agent = db.query(Agent).filter(
        Agent.id == agent_data.agent_id,
        Agent.user_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if agent already in team
    existing = db.query(TeamAgent).filter(
        TeamAgent.team_id == team_id,
        TeamAgent.agent_id == agent_data.agent_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Agent already in team")
    
    team_agent = TeamAgent(
        team_id=team_id,
        agent_id=agent_data.agent_id,
        order=agent_data.order,
        is_manager=agent_data.is_manager
    )
    
    db.add(team_agent)
    db.commit()
    return {"message": "Agent added to team successfully"}

@router.post("/{team_id}/execute")
def execute_team(
    team_id: int,
    execution_data: TeamExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute team workflow"""
    agent_service = AgentService(db)
    
    # Verify team ownership
    team = db.query(Team).filter(
        Team.id == team_id,
        Team.user_id == current_user.id
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    result = agent_service.execute_team(team_id, execution_data.task_description)
    return result

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_update: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update team configuration"""
    team = db.query(Team).filter(
        Team.id == team_id,
        Team.user_id == current_user.id
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Update fields
    for field, value in team_update.dict(exclude_unset=True).items():
        setattr(team, field, value)
    
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete team (soft delete)"""
    team = db.query(Team).filter(
        Team.id == team_id,
        Team.user_id == current_user.id
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team.is_active = False
    db.commit()
    return {"message": "Team deleted successfully"} 