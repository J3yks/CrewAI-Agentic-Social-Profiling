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
class HRCrew:
    """Human Resources department crew"""

    @agent
    def hr_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_manager"],
            tools=[
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    # @agent
    # def hr_business_partner(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["hr_business_partner"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm=gemini_llm
    #     )

    # @agent
    # def hr_junior(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["hr_junior"],
    #         tools=[read_discord_messages,
    #                send_discord_webhook],
    #         verbose=True,
    #         step_callback=_step_callback,
    #         llm=gemini_llm
    #     )

    @task
    def inv_reply(self) -> Task:
        return Task(
            config=self.tasks_config["hr_manager_reply"],
        )
    
    # @task
    # def beh_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["hr_business_partner_reply"],
    #     )

    # @task
    # def soc_reply(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["hr_junior_reply"],
    #     )

    @before_kickoff
    def before_kickoff(self, inputs: dict) -> dict:
        
        return inputs

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.hr_manager(),
                    # self.hr_business_partner(),
                    # self.hr_junior()
                    ],
            tasks=[self.inv_reply(),
                #    self.beh_reply(),
                #    self.soc_reply()
                   ],
            process=Process.sequential,
            verbose=True,
            tracing=True
        )
