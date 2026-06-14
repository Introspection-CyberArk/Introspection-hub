import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Your bots list
BOTS = [
    {"name": "🤖 J.A.R.V.I.S. AI", "username": "@IntroAssist_Bot"},
    {"name": "💱 Currency Exchange Bot", "username": "@currrency_exch_bot"},
    {"name": "🔢 Num Spy Bot", "username": "@Num_Spy_Bot"}
]

@app.route("/", methods=["GET"])
def index():
    return "Bot Hub is running! - @Introspection007"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        # Get the update from Telegram
        update = request.get_json()
        print(f"Update received: {update}")
        
        # Extract message info
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        
        if not chat_id:
            return "", 200
        
        # Prepare reply based on command (using HTML instead of Markdown)
        if text == "/start":
            reply = """<b>🤖 Bot Hub</b>

Welcome to @Introspection007's Bot Hub!

<b>Available Bots:</b>

• <b>J.A.R.V.I.S. AI</b>: @IntroAssist_Bot
• <b>Currency Exchange Bot</b>: @currrency_exch_bot
• <b>Num Spy Bot</b>: @Num_Spy_Bot

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 <b>Powered By @Introspection007</b>

Tap any username above to launch the bot!"""
        
        elif text == "/help":
            reply = """<b>🤖 Bot Hub Help</b>

<b>Commands:</b>
/start - Show all bots
/help - Show this help

<b>How to use:</b>
Simply tap on any bot username to open it!

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 <b>Powered By @Introspection007</b>"""
        
        else:
            reply = """<b>🤖 Bot Hub</b>

Send /start to see all available bots.

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 <b>Powered By @Introspection007</b>"""
        
        # Send the reply back to Telegram using HTML parse mode
        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "HTML"
        }
        
        response = requests.post(send_url, json=payload)
        print(f"Send response status: {response.status_code}")
        print(f"Send response body: {response.text}")
        
        return "", 200
        
    except Exception as e:
        print(f"Error: {e}")
        return "", 200

if __name__ == "__main__":
    app.run()
