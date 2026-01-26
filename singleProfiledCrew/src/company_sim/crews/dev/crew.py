import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM, TaskOutput
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)

from typing import Tuple, Any
load_dotenv()

gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY"), temperature=0.6 )

@CrewBase
class DevCrew:
    """Development department crew"""

    @agent
    def dev_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_manager"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            llm= gemini_llm
        )

    @agent
    def dev_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_junior"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            llm= gemini_llm

        )

    @task
    def devman_reply(self) -> Task:
        return Task(
            config=self.tasks_config["dev_manager_reply"],
        )

    @task
    def devjun_reply(self) -> Task:
        return Task(
            config=self.tasks_config["dev_junior_reply"],
        )

    @crew
    def crew(self) -> Crew:
        """Dev Crew"""
        return Crew(

            agents=[
                self.dev_manager(),
                self.dev_junior()
            ],
            tasks=[
                self.devman_reply(),
                self.devjun_reply()
            ],
            process=Process.sequential,
            cache = False,
            verbose=True
        )
