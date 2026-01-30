import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages
)
from company_sim.utils import discord_logger
load_dotenv()
# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY") )

def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(3)

@CrewBase
class ManCrew:
    """Human Resources department crew"""

    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],
            # tools=[read_discord_messages],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config["manager_task"],
        )

    @before_kickoff
    def before_kickoff(self, inputs: dict) -> dict:
        time.sleep(4)
        return inputs

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.manager()],
            tasks=[self.manager_task()],
            process=Process.sequential,
            verbose=True,
            tracing=True
        )
