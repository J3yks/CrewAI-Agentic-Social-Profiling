import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)
from company_sim.utils import discord_logger
load_dotenv()
# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY") )


def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(3)

@CrewBase
class DevCrew:
    """Development department crew"""

    @agent
    def dev_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_manager"],
            tools=[
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm= gemini_llm
        )

    # @agent
    # def dev_backend(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["dev_backend"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm= gemini_llm

    #     )

    # @agent
    # def dev_junior(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["dev_junior"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm= gemini_llm

    #     )

    @task
    def devman_reply(self) -> Task:
        return Task(
            config=self.tasks_config["dev_manager_reply"],
           # callback = discord_logger.task_callback
        )
    
    # @task
    # def devback_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["dev_backend_reply"],
    #        # callback = discord_logger.task_callback
    #     )

    # @task
    # def devjun_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["dev_junior_reply"],
    #        # callback = discord_logger.task_callback
    #     )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.dev_manager(),
                # self.dev_backend(),
                # self.dev_junior()
            ],
            tasks=[
                self.devman_reply(),
                # self.devback_reply(),
                # self.devjun_reply()
            ],
            process=Process.sequential,
            verbose=True,
            tracing=True
        )
