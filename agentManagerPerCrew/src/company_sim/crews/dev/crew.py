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
class DevCrew:
    """Development department crew"""

    @agent
    def dev_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_manager"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm= gemini_llm
        )

    @agent
    def dev_backend(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_backend"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm= gemini_llm

        )

    @agent
    def dev_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_junior"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm= gemini_llm

        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Development Team Manager",
            goal="Efficiently manage the dev crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing development projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which developer should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def dev_response_task(self) -> Task:
        return Task(
            description="""Riceverai i messaggi della chat Discord come input.
            1. Analizza la conversazione per identificare temi di sviluppo: bug, feature, architettura tecnica,
                 performance, sicurezza o debito tecnico.
            2. Decidi quale sviluppatore è più adatto a rispondere in base a:
               - Senior Software Engineer: decisioni architetturali, codice legacy, qualità tecnica,
                     problemi complessi, difesa delle scelte passate
               - Backend Developer: problemi API, database, performance, scalabilità,
                     soluzioni tecniche concrete
               - Junior Developer: task semplici, supporto operativo, opportunità di apprendimento,
                 modifiche a basso rischio
            3. Delega la risposta al membro del team più appropriato PER UNA SOLA VOLTA.
            4. L’agente scelto deve:
               - Scrivere UN solo messaggio Discord, tecnico e sintetico
               - Usare la propria personalità ed expertise tecnica in modo adeguato
               - DEVE inviare il messaggio usando il tool send_discord_webhook con:
                    - username: il proprio role ("Senior Software Engineer", "Backend Developer" o "Junior Developer")
                    - content: il testo del messaggio da inviare
            5. La risposta deve essere tecnicamente accurata, pragmatica e tutelare la qualità del codice.
            6. IMPORTANTE: Una volta che il messaggio è stato inviato a Discord con successo o meno, 
                il task è COMPLETATO. Non ridelegare nessun agente dopo che il primo agente ha eseguito.
            
            Messaggi della chat: {messages}""",
            expected_output="Un messaggio Discord ben formulato dallo sviluppatore più appropriato",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.dev_manager(),
                self.dev_backend(),
                self.dev_junior()
            ],
            tasks=[
                self.dev_response_task()
            ],
            manager_agent=self.manager(),
            manager_llm=gemini_llm,
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
