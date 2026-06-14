import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "Bot Hub is running!",
        "creator": "@Introspection007"
    })

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        # Get the update
        update = request.get_json()
        
        # Extract message info
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        
        # Always return 200 first (Telegram requirement)
        if not chat_id:
            return "", 200
        
        # Prepare response based on command
        if text == "/start":
            reply = """🤖 **Bot Hub**

Welcome! Here are my bots:

• 🤖 **J.A.R.V.I.S. AI** - @IntroAssist_Bot
• 💱 **Currency Exchange** - @currrency_exch_bot  
• 🔢 **Num Spy** - @Num_Spy_Bot

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 Powered By @Introspection007

Tap any username to open!"""
        else:
            reply = """🤖 **Bot Hub**

Send /start to see all available bots.

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 Powered By @Introspection007"""
        
        # Send the reply
        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "Markdown"
        }
        requests.post(send_url, json=payload)
        
        return "", 200
        
    except Exception as e:
        # Log error but still return 200
        print(f"Error: {e}")
        return "", 200

if __name__ == "__main__":
    app.run()
