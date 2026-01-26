import os
import time
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew
from company_sim.tools.discord_tools import read_discord_messages

# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY"), temperature=0 )


@CrewBase
class ProfilingCrew:
    """User Profiling crew - analyzes Discord messages to profile users"""

    @agent
    def profiler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["profiler_agent"],
            verbose=True,
            llm=gemini_llm
        )

    @task
    def analyze_and_profile(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_and_profile"],
            markdown=True
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.profiler_agent()
            ],
            tasks=[
                self.analyze_and_profile()
            ],
            process=Process.sequential,
            verbose=True
        )
