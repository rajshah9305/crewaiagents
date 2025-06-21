from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = []
    llm_config: Dict[str, Any] = {}
    memory_enabled: bool = True
    allow_delegation: bool = False
    verbose: bool = True

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    backstory: Optional[str] = None
    tools: Optional[List[str]] = None
    llm_config: Optional[Dict[str, Any]] = None
    memory_enabled: Optional[bool] = None
    allow_delegation: Optional[bool] = None
    verbose: Optional[bool] = None

class AgentResponse(AgentBase):
    id: int
    user_id: int
    total_executions: int
    success_rate: int
    avg_response_time: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class TaskExecute(BaseModel):
    task_description: str

class AgentExecutionResult(BaseModel):
    result: str
    execution_time: int
    agent_name: str 