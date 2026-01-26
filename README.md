# CrewAI Agentic Social Profiling
## Abstract

[crewAI](https://crewai.com) Agentic Social Profiling is an automated system designed to analyze and understand relational, behavioral, and communicative dynamics within a corporate or social group. Developed as a project for the Alma Mater Studiorum Università di Bologna (A.Y. 2025-2026), it utilizes a multi-agent framework to move beyond passive data analysis toward active participation by autonomous entities.

By integrating Large Language Models (LLMs) and the [crewAI](https://crewai.com) orchestration framework, the system simulates a corporate chat environment (via Discord) where artificial agents represent specific roles—such as Senior Engineers or HR Managers. These agents interact, interpret context, and deduce "latent dynamics" or "Secret Flags" (unexpressed grievances like technical debt or lack of mentorship). The ultimate goal is to transform raw social data into actionable HR insights, facilitating proactive mediation and team cohesion.

## Project Structure
The repository contains three distinct implementations, each exploring different levels of organizational complexity and agentic autonomy:


**Version 1: Single Profiled Crew** – Focused on a small group to ensure a high density of messages for accurate individual profiling.


**Version 2: Agent Manager per Crew** – Implements a hierarchical architecture where each department has its own manager to coordinate tasks.


**Version 3: General Agent Manager** – A centralized management approach for the entire ecosystem.

Each version is contained within its own directory with a dedicated README.md for specific technical details.

## Prerequisites
To run this project, you will need the following technologies:


**Python >=3.10 <3.14:** The core programming language.


**API KEY:** Serving as the "reasoning engine" for the agents.


**Discord API & Webhooks:** Used for real-time input/output simulation.

**[UV](https://docs.astral.sh/uv/):** A dependency manager and package handler that offers a seamless setup and execution experience.



## Installation
Clone the repository:

```bash
git clone https://github.com/your-repo/crewai-social-profiling.git
cd crewai-social-profiling
```
Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.ps1
```
Install the required dependencies:

```bash
pip install uv
```


Next, navigate to your project directory and install the dependencies:
```bash
crewai install
```
Configuration: Create a `.env` file in the root of the implementation folder you wish to run and add your API credentials:

```env
GEMINI_API_KEY=your_api_key
DISCORD_TOKEN=your_discord_bot_token
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```
## Execution
To start the simulation, navigate to the specific implementation folder and run the main.py script. For example, to run the single crew version:

```bash
cd singleProfiledCrew
crewai run
```
The system follows a three-phase lifecycle:


**Bootstrapping:** Injects an "ice-breaking" message into the Discord channel.


**Execution Loop:** A timed while loop where agents interact and react to messages.


**Reporting:** A dedicated ProfilingCrew analyzes the chat history and generates a report.md file summarizing the discovered social dynamics.
