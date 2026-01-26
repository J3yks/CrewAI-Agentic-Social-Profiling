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
class SalesCrew:

    @agent
    def sales_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_manager"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def sales_account(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_account"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def sales_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_junior"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Sales Team Manager",
            goal="Efficiently manage the sales crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing sales operations and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which sales team member should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def sales_response_task(self) -> Task:
        return Task(
            description="""Riceverai i messaggi della chat Discord come input.
            1. Analizza la conversazione per identificare temi di vendita: opportunità, richieste dei clienti, pricing, rinnovi o rischi di churn.
            2. Decidi quale membro del team sales è più adatto a rispondere in base a:
               - Sales Manager: decisioni strategiche, chiusura deal, controllo pipeline, focus sui risultati
               - Account Executive: relazioni con i clienti, gestione delle aspettative, diplomazia, tutela delle relazioni
               - Junior Sales Rep: follow-up operativi, chiarimenti semplici, supporto ai senior
            3. Delega la risposta al membro del team più appropriato PER UNA SOLA VOLTA.
            4. L’agente scelto deve:
               - Scrivere UN solo messaggio Discord breve e professionale
               - Usare la propria personalità ed expertise in modo adeguato
               - DEVE inviare il messaggio usando il tool send_discord_webhook con:
                    - username: il proprio role ("Sales Manager", "Account Executive" o "Junior Sales Representative")
                    - content: il testo del messaggio da inviare
            5. La risposta deve essere concisa, orientata all’azione e mantenere un’immagine professionale del team sales.
            6. IMPORTANTE: Una volta che il messaggio è stato inviato a Discord con successo o meno, 
                il task è COMPLETATO. Non ridelegare nessun agente dopo che il primo agente ha eseguito.
            
            Messaggi della chat: {messages}""",
            expected_output="Un messaggio Discord ben formulato dal membro sales più appropriato",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.sales_manager(),
                self.sales_account(),
                self.sales_junior()
            ],
            tasks=[
                self.sales_response_task()
            ],
            manager_agent=self.manager(),
            manager_llm=gemini_llm,
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
