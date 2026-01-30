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
from company_sim.crews.manager.crew import ManCrew
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)
import asyncio

from company_sim.utils.discord_logger import send_discord_webhook



warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
 
def post_initial_hr_message():
        """
        Invia il primo messaggio degli HR direttamente via webhook,
        prima di attivare i task CrewAI.
        """
        username = "HR Manager"
        content = (
            "Ciao a tutti! Siamo qui per ascoltare e capire meglio le vostre esigenze. "
            "Come potremmo migliorare la gestione del carico di lavoro e la comunicazione tra reparti? "
            "Cosa vi aiuterebbe di più per sentirvi meglio al lavoro?"
        )
        send_discord_webhook(username, content)

def marketing_turn():
    """
    Esegue i task della crew Marketing.
    Ogni agent decide se e come rispondere.
    """
    print("[TURN] Marketing crew in azione...")
    try:
        messages = read_discord_messages.run(limit=100)
        marketingCrew = MarketingCrew()
        MarketingCrew.crew(marketingCrew).kickoff(inputs={"messages":messages})
    except Exception as e:
        print(f"[ERRORE] Marketing crew: {e}")


def sales_turn():
    """
    Esegue i task della crew Sales.
    """
    print("[TURN] Sales crew in azione...")
    try:
        messages = read_discord_messages.run(limit=100)
        salesCrew = SalesCrew()
        SalesCrew.crew(salesCrew).kickoff(inputs={"messages":messages})
    except Exception as e:
        print(f"[ERRORE] Sales crew: {e}")


def dev_turn():
    """
    Esegue i task della crew Dev.
    """
    print("[TURN] Dev crew in azione...")
    try:
        messages = read_discord_messages.run(limit=100)
        devCrew = DevCrew()
        DevCrew.crew(devCrew).kickoff(inputs={"messages":messages})
    except Exception as e:
        print(f"[ERRORE] Dev crew: {e}")


def hr_turn():
    """
    Esegue i task della crew HR.
    """
    print("[TURN] HR crew in azione...")
    try:
        messages = read_discord_messages.run(limit=100)
        hrCrew = HRCrew()
        HRCrew.crew(hrCrew).kickoff(inputs={"messages":messages})
    except Exception as e:
        print(f"[ERRORE] HR crew: {e}")

def man_turn():
    """
    Esegue i task della crew HR.
    """
    print("[TURN] Man crew in azione...")
    try:
        messages = read_discord_messages.run(limit=100)
        manCrew =ManCrew()
        result = ManCrew.crew(manCrew).kickoff(inputs={"messages":messages})
        return result
    except Exception as e:
        print(f"[ERRORE] Man crew: {e}")

async def run():
    durata_simulazione_secondi = 60*30 
    start_time = time.time()
    print(f"[SYSTEM] Simulazione avviata. Durata prevista: {durata_simulazione_secondi/60} minuti.")
    
    post_initial_hr_message()
    skip_hr = True

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time > durata_simulazione_secondi:
            print(f"\n[SYSTEM] Tempo scaduto ({int(elapsed_time)}s). Chiusura simulazione in corso...")
            break

        # --- LOGICA INTEGRATA CON AGENTE ROUTER ---
        print("[SYSTEM] L'agente Coordinatore sta analizzando la chat per il prossimo turno...")
        
        # Eseguiamo la task di analisi
        result = man_turn()
        print(result)
        # Puliamo l'output (rimuovendo spazi o newline) e lo portiamo in minuscolo per lo switch
        crew_choice = str(result).strip().upper()
        print(f"[DECISIONE] L'agente ha scelto il reparto: {crew_choice}")

        # Mapping della decisione sulle funzioni esistenti
        if "MARKETING" in crew_choice:
            marketing_turn()
            skip_hr = False  
            
        elif "SALES" in crew_choice:
            sales_turn()
            skip_hr = False  

        elif "DEV" in crew_choice:
            dev_turn()
            skip_hr = False  

        elif "HR" in crew_choice:
            
            hr_turn()
            
        
        else:
            print(f"[WARNING] L'agente ha restituito un valore non previsto: {crew_choice}. Scelta casuale di fallback.")
            # Opzionale: fallback casuale se l'LLM sbaglia formato
            fallback = random.choice(["marketing", "sales", "dev"])
            globals()[f"{fallback}_turn"]()

        # --- FINE LOGICA AGENTE ---

        sleep_seconds = random.randint(5, 10)
        print(f"[SIM] Pausa di {sleep_seconds} secondi prima del prossimo turno...\n")
        time.sleep(sleep_seconds)
            
    # Profiling finale
    messages = read_discord_messages.run(limit=100)
    profiling_result = ProfilingCrew().crew().kickoff(inputs={"messages":messages})
    print("\n" + "="*80)
    print("PROFILING REPORT")
    print("="*80)
    print(profiling_result)


def run_crew():
    asyncio.run(run())