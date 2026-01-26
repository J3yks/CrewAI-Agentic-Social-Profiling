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
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY"), temperature=0.2 )



@CrewBase
class MarketingCrew:

    @agent
    def marketing_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_lead"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def growth_marketer(self) -> Agent:
        return Agent(
            config=self.agents_config["growth_marketer"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["content_creator"],
            tools=[send_discord_webhook],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Marketing Team Manager",
            goal="Efficiently manage the marketing crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing marketing campaigns and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which marketing team member should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def marketing_response_task(self) -> Task:
        return Task(
            description="""Riceverai i messaggi della chat Discord come input.
            1. Analizza la conversazione per identificare temi di marketing: brand image, messaging, metriche, campagne, contenuti, percezione utenti o discrepanze tra narrativa ufficiale e realtà.
            2. Decidi quale membro marketing è più adatto a rispondere in base a:
               - Marketing Lead: protezione del brand, controllo della narrativa, messaggi strategici, immagine corporate, controllo dello storytelling
               - Growth Marketer: decisioni data-driven, metriche, conversion funnel, A/B test, performance, impaziente verso feedback qualitativi
               - Content Creator: contenuti creativi, ironia, evidenziare ipocrisie o incoerenze con sarcasmo
            3. Delega la risposta al membro del team più appropriato PER UNA SOLA VOLTA.
            4. L’agente scelto deve:
               - Scrivere UN solo messaggio Discord breve che rifletta la propria personalità
               - Usare il proprio approccio specifico (controllo corporate, ossessione per i dati o sarcasmo creativo)
               - DEVE inviare il messaggio usando il tool send_discord_webhook con:
                    - username: il proprio role ("Marketing Lead", "Growth Marketer" o "Content Creator")
                    - content: il testo del messaggio da inviare
            5. La risposta deve allinearsi alla prospettiva marketing, sondando sottilmente per ottenere più informazioni o per esporre eventuali contraddizioni.
            6. IMPORTANTE: Una volta che il messaggio è stato inviato a Discord con successo o meno, 
                il task è COMPLETATO. Non ridelegare nessun agente dopo che il primo agente ha eseguito.
            
            Messaggi della chat: {messages}""",
            expected_output="Un messaggio Discord ben formulato dal membro marketing più appropriato",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.marketing_lead(),
                self.growth_marketer(),
                self.content_creator()
            ],
            tasks=[
                self.marketing_response_task()
            ],
            manager_agent=self.manager(),
            manager_llm=gemini_llm,
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
