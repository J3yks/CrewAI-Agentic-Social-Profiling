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

from company_sim.utils import discord_logger

# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY") )


def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(3)

@CrewBase
class MarketingCrew:

    @agent
    def marketing_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_lead"],
            tools=[
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    # @agent
    # def growth_marketer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["growth_marketer"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm=gemini_llm
    #     )

    # @agent
    # def content_creator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["content_creator"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm=gemini_llm
    #     )

    @task
    def marketing_lead_reply(self) -> Task:
        return Task(
            config=self.tasks_config["marketing_lead_reply"],
           # callback = discord_logger.task_callback
        )

    # @task
    # def growth_marketer_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["growth_marketer_reply"],
    #       #  callback = discord_logger.task_callback
    #     )
    
    # @task
    # def content_creator_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["content_creator_reply"],
    #       #  callback = discord_logger.task_callback
    #     )

    @before_kickoff
    def before_kickoff(self, inputs: dict) -> dict:
        time.sleep(7)
        return inputs

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.marketing_lead(),
                # self.growth_marketer(),
                # self.content_creator()
            ],
            tasks=[
                self.marketing_lead_reply(),
                # self.growth_marketer_reply(),
                # self.content_creator_reply()
            ],
            process=Process.sequential,
            verbose=True,
            tracing=True
        )
