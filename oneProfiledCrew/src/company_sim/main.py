#!/usr/bin/env python
import random
import sys
import time
import warnings
from datetime import datetime
from company_sim.crews.dev.crew import DevCrew
from company_sim.crews.hr.crew import HRCrew
from company_sim.crews.hr.crew import ProfilingCrew


from company_sim.tools.discord_tools import send_discord_webhook


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
 
def post_initial_hr_message():
        """
        Invia il primo messaggio degli HR direttamente via webhook,
        prima di attivare i task CrewAI.
        """
        username = "HR Manager"
        content = (
            "Ciao a tutti! Mi prendo un momento per fare un salto qui nel vostro canale. "
            "So che l'ultimo periodo è stato intenso e volevo semplicemente capire come sta andando la collaborazione e se c'è qualcosa che l'HR può fare per supportarvi meglio nel quotidiano. "
            "Come vi sentite rispetto al lavoro attuale?"
        )
        send_discord_webhook.func(username, content)

def run_crew():
    durata_simulazione_secondi = 900
    start_time = time.time()
    print(f"[SYSTEM] Simulazione avviata. Durata prevista: {durata_simulazione_secondi/60} minuti.")
    post_initial_hr_message()
    
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > durata_simulazione_secondi:
            print(f"\n[SYSTEM] Tempo scaduto ({int(elapsed_time)}s). Chiusura simulazione...")
            break
        
        # --- ESECUZIONE DEV ---
        try:
            DevCrew().crew().kickoff()
        except Exception as e:
            print(f"\nErrore DevCrew (saltato): {e}")

        # --- ESECUZIONE HR ---
        try:
            HRCrew().crew().kickoff() 
        except Exception as e:
            print(f"\nErrore HRCrew (saltato): {e}")

        time.sleep(2) 
            
    # --- PROFILING FINALE ---
    print("\n[SYSTEM] Avvio fase di profiling finale...")
    try:
        profiling_result = ProfilingCrew().crew().kickoff()
        print("\n" + "="*80)
        print("PROFILING REPORT")
        print("="*80)
        print(profiling_result.raw)
    except Exception as e:
        print(f"Errore critico nel profiling finale: {e}")
if __name__ == "__main__":
    run_crew()