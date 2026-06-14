import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Your bots list
BOTS = [
    {"name": "J.A.R.V.I.S. AI", "username": "@IntroAssist_Bot"},
    {"name": "Currency Exchange Bot", "username": "@currrency_exch_bot"},
    {"name": "Num Spy Bot", "username": "@Num_Spy_Bot"}
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
        
        # Prepare reply based on command
        if text == "/start":
            reply = "🤖 *Bot Hub*\n\nWelcome to @Introspection007's Bot Hub!\n\n*Available Bots:*\n"
            for bot in BOTS:
                reply += f"\n• {bot['name']}: {bot['username']}"
            reply += "\n\n━━━━━━━━━━━━━━━━━━━━━\n👨‍💻 *Powered By @Introspection007*"
        
        elif text == "/help":
            reply = "🤖 *Bot Hub Help*\n\n*Commands:*\n/start - Show all bots\n/help - Show this help\n\n━━━━━━━━━━━━━━━━━━━━━\n👨‍💻 *Powered By @Introspection007*"
        
        else:
            reply = "🤖 *Bot Hub*\n\nSend /start to see all available bots.\n\n━━━━━━━━━━━━━━━━━━━━━\n👨‍💻 *Powered By @Introspection007*"
        
        # Send the reply back to Telegram
        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "Markdown"
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
