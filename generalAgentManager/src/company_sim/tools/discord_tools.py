from crewai.tools import tool
import os
import requests

# Token diversi per ogni bot
DISCORD_TOKEN_DEV = os.getenv("DISCORD_TOKEN_DEV")
DISCORD_TOKEN_HR = os.getenv("DISCORD_TOKEN_HR")
DISCORD_TOKEN_MARKETING = os.getenv("DISCORD_TOKEN_MARKETING")
CHANNEL_ID = os.getenv("DISCORD_GAME_CHANNEL_ID")

BASE_URL = "https://discord.com/api/v10"


def _headers(token):
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }


@tool
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


@tool
def post_to_discord_dev(message: str) -> str:
    """
    Posts a message to the Discord channel as the DEV bot.
    """
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/messages"
    payload = {"content": message}

    resp = requests.post(url, headers=_headers(DISCORD_TOKEN_DEV), json=payload)
    resp.raise_for_status()

    return "Message successfully sent to Discord as DEV bot."


@tool
def post_to_discord_hr(message: str) -> str:
    """
    Posts a message to the Discord channel as the HR bot.
    """
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/messages"
    payload = {"content": message}

    resp = requests.post(url, headers=_headers(DISCORD_TOKEN_HR), json=payload)
    resp.raise_for_status()

    return "Message successfully sent to Discord as HR bot."


@tool
def post_to_discord_marketing(message: str) -> str:
    """
    Posts a message to the Discord channel as the MARKETING bot.
    """
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/messages"
    payload = {"content": message}

    resp = requests.post(url, headers=_headers(DISCORD_TOKEN_MARKETING), json=payload)
    resp.raise_for_status()

    return "Message successfully sent to Discord as MARKETING bot."


@tool
def post_to_discord(message: str) -> str:
    """
    Posts a message to the Discord channel.
    (Legacy - usa il token DEV di default)
    """
    return post_to_discord_dev(message)


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
