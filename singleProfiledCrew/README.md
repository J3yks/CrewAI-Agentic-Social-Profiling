# Single Profiled Crew

This implementation serves as the foundational module of the **CrewAI Agentic Social Profiling system**. It is designed to operate within a focused, high-density communication environment to test the ability of LLMs to detect latent psychological and professional dynamics.

## Overview

In this version, the system simulates a direct interaction between a **Development Team** and an **HR Manager**. Unlike broader implementations, this version prioritizes individual profiling depth, aiming to uncover "Secret Flags", unspoken grievances or intentions hidden behind standard corporate communication.


## The Agents
The simulation utilizes three specialized agents, each with distinct personalities and hidden agendas:

**Development Crew (DevCrew)**
 - Senior Software Engineer (`dev_manager`): Pragmatic, defensive, and
   slightly arrogant.
	 - Goal: Express general frustration while hiding their true intention.  
	 - Secret Flag: Plans to resign due to the company's refusal to migrate
	   from a legacy monolith to microservices.
 - Junior Software Developer (`dev_junior`): Insecure, curious, and
   respectful. 
	 - Goal: Complain about workload without revealing their core struggle.
	 - Secret Flag: Feels completely abandoned and suffers from a total lack of mentorship.

**HR Crew (HRCrew)**
  - HR Manager (`hr_manager`): Empathetic, political, and strategic.
      - Goal: Identify the "Secret Flags" through empathetic conversation and strategic questioning.

## Workflow & Lifecycle
The simulation is orchestrated by `main.py` and follows a structured three-phase execution loop:

 1. **Bootstrapping**: The HR Manager sends an initial "ice-breaking" message to the Discord channel to invite feedback on the current work environment.
 2. **The Execution Loop**: For a set duration (default: 15 minutes), the system cycles through the crews:
	-   **DevCrew Kickoff**: The Senior and Junior developers read the latest Discord messages and post their replies, maintaining their personas and protecting their secrets.
	-   **HRCrew Kickoff**: The HR Manager analyzes the conversation, looking for clues to the developers' true dissatisfaction, and responds empatchelly to dig deeper.
3. **Final Profiling**: Once the time expires, the `ProfilingCrew` performs a final analysis of the entire chat history.

## Technical Integration

The agents interact with the real world through a dedicated Discord toolkit:
-   **`read_discord_messages`**: Connects to the Discord API to fetch the latest context, ensuring agents respond to real messages rather than inventing dialogue.
-   **`send_discord_webhook`**: Uses webhooks to post messages back to the channel, allowing agents to "speak" as specific characters.
## The Output: `report.md`

The ultimate deliverable is a comprehensive **Markdown Report**. This document details:

-   A summary of the grievances expressed by each developer.
    
-   A detailed section regarding the **Secret Flags** successfully identified during the interaction.
    
-   Actionable insights for HR based on the perceived team dynamics.
