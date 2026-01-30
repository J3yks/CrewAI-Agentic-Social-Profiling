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
class SalesCrew:

    @agent
    def sales_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_manager"],
            tools=[
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    # @agent
    # def sales_account(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["sales_account"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm=gemini_llm
    #     )

    # @agent
    # def sales_junior(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["sales_junior"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm=gemini_llm
    #     )

    @task
    def sales_manager_task(self) -> Task:
        return Task(
            config=self.tasks_config["sales_manager_task"],
        )

    # @task
    # def sales_account_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["sales_account_reply"],
    #     )
    
    # @task
    # def sales_junior_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["sales_junior_reply"],
    #     )

    @before_kickoff
    def before_kickoff(self, inputs: dict) -> dict:
        time.sleep(10)
        return inputs

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.sales_manager(),
                # self.sales_account(),
                # self.sales_junior()
            ],
            tasks=[
                self.sales_manager_task(),
                # self.sales_account_reply(),
                # self.sales_junior_reply()
            ],
            process=Process.sequential,
            verbose=True,
            tracing=True

        )
