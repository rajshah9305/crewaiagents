import os
from typing import AsyncGenerator, Dict, Any
from cerebras.cloud.sdk import Cerebras
from crewai import Agent, LLM, Task, Crew
import asyncio
import time
import json

class CerebrasService:
    def __init__(self):
        self.client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))
        self.llm_configs = {
            "fast_chat": {
                "model": "llama-4-scout-17b-16e-instruct",
                "temperature": 0.2,
                "max_completion_tokens": 4096
            },
            "creative": {
                "model": "llama3.1-8b", 
                "temperature": 0.7,
                "max_completion_tokens": 8192
            },
            "analytical": {
                "model": "llama3.1-70b",
                "temperature": 0.1,
                "max_completion_tokens": 8192
            }
        }
    
    def get_crewai_llm(self, config_type: str = "fast_chat") -> LLM:
        """Get CrewAI compatible LLM instance"""
        config = self.llm_configs.get(config_type, self.llm_configs["fast_chat"])
        return LLM(
            model=f"cerebras/{config['model']}",
            api_key=os.environ.get("CEREBRAS_API_KEY"),
            base_url="https://api.cerebras.ai/v1",
            temperature=config["temperature"],
            max_tokens=config["max_completion_tokens"]
        )
    
    async def stream_response(self, messages: list, config_type: str = "fast_chat") -> AsyncGenerator[str, None]:
        """Stream response from Cerebras"""
        config = self.llm_configs.get(config_type, self.llm_configs["fast_chat"])
        
        stream = self.client.chat.completions.create(
            messages=messages,
            model=config["model"],
            stream=True,
            temperature=config["temperature"],
            max_completion_tokens=config["max_completion_tokens"]
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def create_agent(self, agent_data: Dict[str, Any]) -> Agent:
        """Create CrewAI agent with Cerebras LLM"""
        llm_config = agent_data.get("llm_config", {})
        config_type = llm_config.get("config_type", "fast_chat")
        
        return Agent(
            role=agent_data["role"],
            goal=agent_data["goal"], 
            backstory=agent_data["backstory"],
            llm=self.get_crewai_llm(config_type),
            tools=self._get_tools(agent_data.get("tools", [])),
            memory=agent_data.get("memory_enabled", True),
            allow_delegation=agent_data.get("allow_delegation", False),
            verbose=agent_data.get("verbose", True)
        )
    
    def _get_tools(self, tool_names: list):
        """Get actual tool instances based on names"""
        # Import CrewAI tools based on names
        from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool
        
        tool_mapping = {
            "web_search": SerperDevTool(),
            "web_scrape": ScrapeWebsiteTool(),
            "file_read": FileReadTool()
        }
        
        return [tool_mapping[name] for name in tool_names if name in tool_mapping] 