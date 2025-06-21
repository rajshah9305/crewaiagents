from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .agent import AgentResponse

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    process_type: str = "sequential"

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    process_type: Optional[str] = None

class TeamResponse(TeamBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    agents: List[AgentResponse] = []
    
    class Config:
        from_attributes = True

class TeamAgentAdd(BaseModel):
    agent_id: int
    order: int = 0
    is_manager: bool = False

class TeamExecutionRequest(BaseModel):
    task_description: str 