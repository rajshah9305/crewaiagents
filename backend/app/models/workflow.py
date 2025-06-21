from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    workflow_definition = Column(JSON, default=dict)  # React Flow definition
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class WorkflowNode(Base):
    __tablename__ = "workflow_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    node_id = Column(String(100), nullable=False)  # React Flow node ID
    node_type = Column(String(50), nullable=False)  # agent, task, condition
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    data = Column(JSON, default=dict)  # Node data
    config = Column(JSON, default=dict)  # Node configuration

class WorkflowEdge(Base):
    __tablename__ = "workflow_edges"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    edge_id = Column(String(100), nullable=False)  # React Flow edge ID
    source_node_id = Column(String(100), nullable=False)
    target_node_id = Column(String(100), nullable=False)
    source_handle = Column(String(100))
    target_handle = Column(String(100))
    edge_type = Column(String(50), default="default") 