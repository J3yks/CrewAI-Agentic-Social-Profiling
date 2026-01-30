# Multi-Crew Manager-Orchestrated Profiling

This repository implements an advanced version of the **CrewAI Agentic Social Profiling system**, designed to simulate realistic organizational dynamics across multiple departments under hierarchical control.

The system emphasizes **centralized context ingestion**, manager-mediated agent selection, and agent-driven message production through tool usage.

----------

## Overview

The simulation models a multi-department organization composed of four operational crews — **Development, HR, Sales, and Marketing** — interacting within a shared communication channel.

At each iteration, the **chat history is retrieved once by the orchestration layer** and injected as immutable context into a selected crew.  
Agents do not read the chat directly: all reasoning is performed on the provided context snapshot.

Each crew is coordinated by an **Agent Manager** that does not participate in the conversation, but instead analyzes the context and selects which operational agent should intervene.

A separate **ProfilingCrew**, external to the interaction loop, is activated only at the end of the simulation to perform post-hoc analysis.

----------

## The Crews and Agents

### Operational Crews

Each operational crew follows a hierarchical structure:

-   **1 Agent Manager** (silent orchestrator)
    
-   **Operational Agents** (conversational actors)
    

Only operational agents produce messages in the chat and do so **exclusively via tool invocation**.

**Development Crew (DevCrew)**

-   Senior Software Engineer
    
-   Backend Developer
    
-   Junior Software Developer
    

**HR Crew (HRCrew)**

-   HR Specialist
    

**Sales Crew (SalesCrew)**

-   Sales Manager
    
-   Account Executive
    
-   Junior Sales Representative
    

**Marketing Crew (MarketingCrew)**

-   Head of Marketing
    
-   Growth Marketer
    
-   Content Specialist
    

Each agent is characterized by a role, a goal, a backstory, and one or more **Secret Flags**.

----------

### Profiling Crew (ProfilingCrew)

The **ProfilingCrew** consists of a single analytical agent without a Manager and does not participate in the conversational loop.

It is activated only once, after the interaction phase ends, to analyze the complete chat history.

----------

## Workflow & Lifecycle

The simulation is orchestrated by `main.py` and governed by a **time-bounded while loop**.

1.  **Bootstrapping**  
    An initial context-setting message is injected into the communication channel to initiate interaction.
    
2.  **Dynamic Execution Loop**  
    For the duration of the simulation:
    
    -   the orchestration layer retrieves the chat history once per iteration via `read_discord_messages`;
        
    -   one operational crew is selected randomly (Dev, HR, Sales, or Marketing);
        
    -   the retrieved chat snapshot is injected as context into the selected crew;
        
    -   the crew is executed through `kickoff()`.
        
    
    Within the crew, the **Agent Manager** selects a single operational agent to respond.
    
    The selected agent generates its message by invoking the `send_discord_webhook` tool.
    
3.  **Final Profiling Phase**  
    Once the time limit expires, the **ProfilingCrew** performs a global, non-interfering analysis of the entire conversation.
    

----------

## Tooling and External Integration

-   **`read_discord_messages`**  
    Used exclusively by the orchestration layer to retrieve real Discord messages and construct a shared context snapshot.
    
-   **`send_discord_webhook`**  
    Exposed as a tool to operational agents, enabling them to publish messages to Discord in a controlled and traceable manner.
    

This separation enforces a clear boundary between **context acquisition**, **decision-making**, and **message emission**.

----------

## Output: `report.md`

The final output is a structured **Markdown report** containing:

-   crew-level behavioral summaries;
    
-   identified **Secret Flags** with supporting conversational evidence;
    
-   cross-department tension analysis;
    
-   observations on managerial orchestration and agent selection;
    
-   limitations related to context snapshotting, timing constraints, and model compliance.
