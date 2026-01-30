import os
import requests
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def _send_webhook(username, content):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ Warning: Nessun Webhook URL trovato nel file .env")
        return

    data = {
        "username": username,
        "content": content
        # "avatar_url": avatar_url
    }
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Errore Discord: {e}")

def task_callback(output):
    """
    Questa è l'unica funzione che importerai nel main.
    """
    # Logica di formattazione
    agent_role = output.agent
    content = output.raw
    
    # Tronca se troppo lungo
    if len(content) > 1900:
        content = content[:1900] + "...\n*(Vedi output completo in console)*"
        
    # Recupera avatar
    # avatar = AGENT_AVATARS.get(agent_role)
    
    # Invia
    _send_webhook(agent_role, content)

def send_discord_webhook(username: str, content: str) -> str:
    """
    Sends a message to Discord using a webhook.
    Args:
        username: The name that will appear as the sender
        content: The message content to send
    Returns:
        Success or error message
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return "⚠️ Error: DISCORD_WEBHOOK_URL not found in .env"

    # Tronca se troppo lungo
    if len(content) > 1900:
        content = content[:1900] + "...\n*(Message truncated)*"
    
    data = {
        "username": username,
        "content": content
    }
    
    try:
        resp = requests.post(webhook_url, json=data)
        resp.raise_for_status()
        return f" Message sent to Discord as {username}"
    except Exception as e:
        return f" Error sending to Discord: {e}"


def read_discord_messages(limit: int = 100) -> str:
    """
    Reads the latest messages from the Discord channel.
    Returns a formatted plain-text chat log.
    """
    # Usa il primo token disponibile per leggere
    token = DISCORD_TOKEN_DEV or DISCORD_TOKEN_HR or DISCORD_TOKEN_MARKETING
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/messages"
    params = {"limit": limit}

    resp = requests.get(url, headers=_headers(token), params=params)
    resp.raise_for_status()

    messages = resp.json()
    messages.reverse()

    return "\n".join(
        f"{m['author']['username']}: {m['content']}"
        for m in messages
        if m["content"]
    )