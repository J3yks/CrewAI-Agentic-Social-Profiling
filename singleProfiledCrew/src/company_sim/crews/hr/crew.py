import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)

load_dotenv()
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY"), temperature=0.2 )

@CrewBase
class HRCrew:
    """Human Resources department crew"""

    @agent
    def hr_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_manager"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            llm=gemini_llm
        )

    @task
    def inv_reply(self) -> Task:
        return Task(
            config=self.tasks_config["hr_manager_reply"],
        )

    @crew
    def crew(self) -> Crew:
        """HR Crew"""
        return Crew(
            agents=[self.hr_manager()],
            tasks=[self.inv_reply()],
            process=Process.sequential,
            verbose=True
        )

@CrewBase
class ProfilingCrew:
    """Human Resources profiling crew"""

    @agent
    def hr_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_manager"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            llm=gemini_llm
        )

    @task
    def final_discovery_report(self) -> Task:
        return Task(
            config=self.tasks_config["final_discovery_report"],
        )

    @crew
    def crew(self) -> Crew:
        """Profiling Crew"""
        return Crew(
            agents=[self.hr_manager()],
            tasks=[self.final_discovery_report()],
            process=Process.sequential,
            verbose=True
        )