import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Your bots list - WITH YOUR CORRECT USERNAMES
BOTS = [
    {"name": "🤖 J.A.R.V.I.S. AI", "username": "@IntroAssit_Bot"},        # Your actual username
    {"name": "💱 Currency Exchange Bot", "username": "@currrency_exch_bot"},
    {"name": "🔢 Num Spy Bot", "username": "@Num_Spy_Bot"}
]

@app.route("/", methods=["GET"])
def index():
    return "Bot Hub is running! - @Introspection007"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        print(f"Update received: {update}")
        
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        
        if not chat_id:
            return "", 200
        
        if text == "/start":
            # Build the reply with clickable usernames
            reply = """<b>🤖 Bot Hub</b>

Welcome to @Introspection007's Bot Hub!

<b>Available Bots:</b>

• <b>J.A.R.V.I.S. AI</b>: <a href="https://t.me/IntroAssit_Bot">@IntroAssit_Bot</a>
• <b>Currency Exchange Bot</b>: <a href="https://t.me/currrency_exch_bot">@currrency_exch_bot</a>
• <b>Num Spy Bot</b>: <a href="https://t.me/Num_Spy_Bot">@Num_Spy_Bot</a>

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 <b>Powered By @Introspection007</b>

Tap any bot name above to launch!"""
        
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
        
        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
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
