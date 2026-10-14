"""bot.py — Slack bot with OpenAI via Bolt Socket Mode.

Companion code for https://stackpractices.com/recipes/slack-bot-openai/
"""

import os

from dotenv import load_dotenv
from openai import OpenAI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

conversations = {}


def get_history(user_id):
    if user_id not in conversations:
        conversations[user_id] = [
            {"role": "system", "content": "You are a helpful assistant in a Slack workspace."}
        ]
    return conversations[user_id]


def get_gpt_response(messages):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
    )
    return response.choices[0].message.content


@app.event("app_mention")
def handle_mention(event, say):
    import re

    text = re.sub(r"<@[^>]+>", "", event["text"]).strip()
    if not text:
        return  # bare mention with no question
    history = get_history(event["user"])
    history.append({"role": "user", "content": text})
    reply = get_gpt_response(history)
    history.append({"role": "assistant", "content": reply})
    if len(history) > 11:
        conversations[event["user"]] = [history[0]] + history[-10:]
    say(text=reply, thread_ts=event["ts"])


@app.message("")
def handle_dm(message, say):
    # Skip bots, non-DM traffic, and empty text
    if message.get("bot_id") or message.get("subtype") or message.get("channel_type") != "im":
        return
    if not message.get("text", "").strip():
        return
    history = get_history(message["user"])
    history.append({"role": "user", "content": message["text"]})
    reply = get_gpt_response(history)
    history.append({"role": "assistant", "content": reply})
    say(reply)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
