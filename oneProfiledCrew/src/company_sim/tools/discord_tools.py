from crewai.tools import tool
import os
import requests

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_GAME_CHANNEL_ID")

BASE_URL = "https://discord.com/api/v10"


def _headers(token):
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }


@tool
def read_discord_messages() -> str:
    """
    Reads the latest messages from the Discord channel.
    Returns a formatted plain-text chat log.
    """
    limit=10
    token = DISCORD_TOKEN
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

@tool
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
