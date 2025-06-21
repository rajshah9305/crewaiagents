from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.workflow import Workflow, WorkflowNode, WorkflowEdge
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class WorkflowCreate(BaseModel):
    name: str
    description: str = ""
    definition: Dict[str, Any] = {}

class WorkflowResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    workflow_definition: Dict[str, Any]
    is_active: bool
    
    class Config:
        from_attributes = True

@router.post("/", response_model=WorkflowResponse)
def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new workflow"""
    workflow = Workflow(
        user_id=current_user.id,
        name=workflow_data.name,
        description=workflow_data.description,
        workflow_definition=workflow_data.definition
    )
    
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow

@router.get("/", response_model=List[WorkflowResponse])
def get_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's workflows"""
    workflows = db.query(Workflow).filter(
        Workflow.user_id == current_user.id,
        Workflow.is_active == True
    ).all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete workflow (soft delete)"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow.is_active = False
    db.commit()
    return {"message": "Workflow deleted successfully"} 