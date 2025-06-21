from sqlalchemy.orm import Session
from app.models.agent import Agent, Team, TeamAgent
from app.services.cerebras_service import CerebrasService
from crewai import Crew, Task
from typing import List, Dict, Any
import json
import time
from fastapi import HTTPException

class AgentService:
    def __init__(self, db: Session):
        self.db = db
        self.cerebras = CerebrasService()
    
    def create_agent(self, user_id: int, agent_data: Dict[str, Any]) -> Agent:
        """Create new agent with Cerebras integration"""
        # Set default LLM config for Cerebras
        if not agent_data.get("llm_config"):
            agent_data["llm_config"] = {
                "config_type": "fast_chat",
                "model": "llama-4-scout-17b-16e-instruct"
            }
        
        db_agent = Agent(
            user_id=user_id,
            name=agent_data["name"],
            role=agent_data["role"],
            goal=agent_data["goal"],
            backstory=agent_data["backstory"],
            tools=agent_data.get("tools", []),
            llm_config=agent_data["llm_config"],
            memory_enabled=agent_data.get("memory_enabled", True),
            allow_delegation=agent_data.get("allow_delegation", False),
            verbose=agent_data.get("verbose", True)
        )
        
        self.db.add(db_agent)
        self.db.commit()
        self.db.refresh(db_agent)
        return db_agent
    
    def execute_single_agent(self, agent_id: int, task_description: str) -> Dict[str, Any]:
        """Execute single agent task"""
        start_time = time.time()
        
        # Get agent from database
        db_agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
        if not db_agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Create CrewAI agent
        crewai_agent = self.cerebras.create_agent({
            "role": db_agent.role,
            "goal": db_agent.goal,
            "backstory": db_agent.backstory,
            "tools": db_agent.tools,
            "llm_config": db_agent.llm_config,
            "memory_enabled": db_agent.memory_enabled,
            "allow_delegation": db_agent.allow_delegation,
            "verbose": db_agent.verbose
        })
        
        # Create task
        task = Task(
            description=task_description,
            agent=crewai_agent,
            expected_output="A comprehensive response to the given task"
        )
        
        # Execute task
        crew = Crew(agents=[crewai_agent], tasks=[task])
        result = crew.kickoff()
        
        # Update agent performance metrics
        execution_time = int((time.time() - start_time) * 1000)  # milliseconds
        self._update_agent_metrics(db_agent, execution_time, success=True)
        
        return {
            "result": str(result),
            "execution_time": execution_time,
            "agent_name": db_agent.name
        }
    
    def execute_team(self, team_id: int, task_description: str) -> Dict[str, Any]:
        """Execute team of agents"""
        # Get team and agents
        team = self.db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        team_agents = self.db.query(TeamAgent).filter(
            TeamAgent.team_id == team_id
        ).order_by(TeamAgent.order).all()
        
        if not team_agents:
            raise HTTPException(status_code=400, detail="No agents in team")
        
        # Create CrewAI agents
        crewai_agents = []
        for team_agent in team_agents:
            agent_data = {
                "role": team_agent.agent.role,
                "goal": team_agent.agent.goal,
                "backstory": team_agent.agent.backstory,
                "tools": team_agent.agent.tools,
                "llm_config": team_agent.agent.llm_config,
                "memory_enabled": team_agent.agent.memory_enabled,
                "allow_delegation": team_agent.agent.allow_delegation,
                "verbose": team_agent.agent.verbose
            }
            crewai_agents.append(self.cerebras.create_agent(agent_data))
        
        # Create tasks for team
        tasks = [
            Task(
                description=f"{task_description} (handled by {agent.role})",
                agent=agent,
                expected_output="A comprehensive response to your assigned part of the task"
            ) for agent in crewai_agents
        ]
        
        # Execute team
        crew = Crew(
            agents=crewai_agents,
            tasks=tasks,
            process=team.process_type
        )
        
        result = crew.kickoff()
        
        return {
            "result": str(result),
            "team_name": team.name,
            "agents_count": len(crewai_agents)
        }
    
    def _update_agent_metrics(self, agent: Agent, execution_time: int, success: bool):
        """Update agent performance metrics"""
        agent.total_executions += 1
        if success:
            # Calculate new success rate
            success_count = int(agent.success_rate * (agent.total_executions - 1) / 100)
            success_count += 1
            agent.success_rate = int((success_count / agent.total_executions) * 100)
            
            # Update average response time
            if agent.avg_response_time == 0:
                agent.avg_response_time = execution_time
            else:
                agent.avg_response_time = int(
                    (agent.avg_response_time + execution_time) / 2
                )
        
        self.db.commit() 