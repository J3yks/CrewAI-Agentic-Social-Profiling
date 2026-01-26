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
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY"), temperature=0.2 )

@CrewBase
class HRCrew:
    """Human Resources department crew"""

    @agent
    def hr_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_manager"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="HR Team Manager",
            goal="Efficiently manage the HR crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing HR operations and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which HR team member should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def hr_response_task(self) -> Task:
        return Task(
            description="""Riceverai i messaggi della chat Discord come input.
            1. Analizza la conversazione per identificare segnali HR: stress, burnout, conflitti, rischi di retention, dinamiche di team o disallineamento tra team.
            2. Delega la risposta all'unico membro del team PER UNA SOLA VOLTA.
            3. L’agente scelto deve:
               - Scrivere UN solo messaggio Discord, breve ed empatico
               - Usare domande aperte per ottenere più informazioni SENZA sembrare un interrogatorio
               - DEVE inviare il messaggio usando il tool send_discord_webhook con:
                    - username: il proprio role ("HR Manager")
                    - content: il testo del messaggio da inviare
            4. DEVE inviare il messaggio usando il tool send_discord_webhook con il nome del proprio role come primo parametro e il testo del messaggio come secondo parametro; NON fornire una risposta finale senza prima chiamare il tool.
            5. IMPORTANTE: Una volta che il messaggio è stato inviato a Discord con successo o meno, 
                il task è COMPLETATO. Non ridelegare nessun agente dopo che il primo agente ha eseguito.
            
            Messaggi della chat: {messages}""",
            expected_output="Un messaggio Discord ben formulato dal membro HR più appropriato",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.hr_manager()],
            tasks=[self.hr_response_task()],
            manager_agent=self.manager(),
            manager_llm=gemini_llm,
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
