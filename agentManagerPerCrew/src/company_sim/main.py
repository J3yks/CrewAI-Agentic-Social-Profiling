#!/usr/bin/env python
import random
import sys
import time
import warnings
from datetime import datetime
from company_sim.crews.dev.crew import DevCrew
from company_sim.crews.hr.crew import HRCrew
from company_sim.crews.marketing.crew import MarketingCrew
from company_sim.crews.sales.crew import SalesCrew
from company_sim.crews.profiling.crew import ProfilingCrew
import asyncio

from company_sim.utils.discord_logger import send_discord_webhook
from company_sim.tools.discord_tools import read_discord_messages



warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
 
def post_initial_hr_message():
        """
        Invia il primo messaggio degli HR direttamente via webhook,
        prima di attivare i task CrewAI.
        """
        username = "HR Manager"
        content = (
            "Ciao a tutti! Mi prendo un momento per fare un salto qui nel vostro canale. So che l'ultimo periodo è stato intenso e volevo semplicemente capire come sta andando la collaborazione e se c'è qualcosa che l'HR può fare per supportarvi meglio nel quotidiano. Come vi sentite rispetto al lavoro attuale?"
        )
        send_discord_webhook(username, content)

def marketing_turn():
    """
    Esegue i task della crew Marketing.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] Marketing crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        marketingCrew = MarketingCrew()
        MarketingCrew.crew(marketingCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] Marketing crew: {e}")


def sales_turn():
    """
    Esegue i task della crew Sales.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] Sales crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        salesCrew = SalesCrew()
        SalesCrew.crew(salesCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] Sales crew: {e}")


def dev_turn():
    """
    Esegue i task della crew Dev.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] Dev crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        devCrew = DevCrew()
        DevCrew.crew(devCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] Dev crew: {e}")


def hr_turn():
    """
    Esegue i task della crew HR.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] HR crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        hrCrew = HRCrew()
        HRCrew.crew(hrCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] HR crew: {e}")

async def run():

    durata_simulazione_secondi = 1200 
    start_time = time.time()
    print(f"[SYSTEM] Simulazione avviata. Durata prevista: {durata_simulazione_secondi/60} minuti.")
    post_initial_hr_message()
    skip_hr = True
    previous_crew = None  # Traccia la crew del turno precedente

    while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > durata_simulazione_secondi:
                print(f"\n[SYSTEM] Tempo scaduto ({int(elapsed_time)}s). Chiusura simulazione in corso...")
                break
            
            # Crea la lista di crew disponibili escludendo quella precedente
            available_crews = ["marketing", "sales", "dev", "hr"]
            if previous_crew:
                available_crews.remove(previous_crew)
            
            crew_choice = random.choice(available_crews)

            if crew_choice == "marketing":
                marketing_turn()
                skip_hr = False  
            
            elif crew_choice == "sales":
                sales_turn()
                skip_hr = False  

            elif crew_choice == "dev":
                dev_turn()
                skip_hr = False  

            elif crew_choice == "hr" and not skip_hr:
                hr_turn()
            
            # Aggiorna la crew precedente solo se effettivamente eseguita
            if crew_choice != "hr" or not skip_hr:
                previous_crew = crew_choice

            # Sleep per non spammare la chat, es. 30-90 secondi
            sleep_seconds = random.randint(1, 2)
            print(f"[SIM] Pausa di {sleep_seconds} secondi prima del prossimo turno...\n")
            time.sleep(sleep_seconds)
            
    print("[TURN] Profiling crew in azione...")
    max_retries = 3
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            # Leggi i messaggi Discord usando il metodo run() del tool
            messages = read_discord_messages.run(limit=100)
            
            print(f"[PROFILING] Tentativo {attempt + 1}/{max_retries}...")
            
            # Passa i messaggi come input alla crew
            profiling_result = ProfilingCrew().crew().kickoff(inputs={'messages': messages})
            break  # Successo, esci dal loop
            
        except Exception as e:
            print(f"[ERRORE] Profiling crew (tentativo {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                print(f"[PROFILING] Retry tra {retry_delay} secondi...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Backoff esponenziale
            else:
                print("[PROFILING] Tutti i tentativi falliti. Salvando i messaggi raccolti...")
                profiling_result = f"# Report di Profilazione\n\n## Errore\n\nImpossibile completare l'analisi a causa di timeout LLM.\n\n## Messaggi Raccolti\n\n{messages}"
    
    if profiling_result:
        print("\n" + "="*80)
        print("PROFILING REPORT")
        print("="*80)
        print(profiling_result)
        
        # Salva il report su file
        try:
            with open('profiling_report.md', 'w', encoding='utf-8') as f:
                f.write(str(profiling_result))
            print(f"\n[SYSTEM] Report salvato in: profiling_report.md")
        except Exception as e:
            print(f"[ERRORE] Impossibile salvare il report: {e}")


def run_crew():
    asyncio.run(run())