import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Your bots list
BOTS = [
    {"id": "jarvis", "name": "🤖 J.A.R.V.I.S. AI", "username": "@IntroAssist_Bot", "category": "AI"},
    {"id": "currency", "name": "💱 Currency Exchange Bot", "username": "@currrency_exch_bot", "category": "Finance"},
    {"id": "numspy", "name": "🔢 Num Spy Bot", "username": "@Num_Spy_Bot", "category": "Utility"}
]

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "Bot Hub is running!",
        "creator": "@Introspection007",
        "bots_count": len(BOTS),
        "bots": BOTS
    })

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        # Get the update from Telegram
        update = request.get_json()
        print(f"Received update: {json.dumps(update)}")  # Log for debugging
        
        # Extract message info
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        
        if not chat_id:
            return jsonify({"status": "ok"}), 200
        
        # Handle /start command
        if text == "/start":
            reply = f"""🤖 **Bot Hub**

Welcome to @Introspection007's Bot Hub!

**Available Bots:**

"""
            for bot in BOTS:
                reply += f"• {bot['name']}: {bot['username']}\n"
            
            reply += """
━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**
            
Tap any username above to launch the bot!"""
        
        elif text == "/help":
            reply = """🤖 **Bot Hub Help**

**Commands:**
/start - Show all bots
/help - Show this help

**How to use:**
Simply tap on any bot username to open it!

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
        
        else:
            reply = f"""🤖 **Bot Hub**

Send /start to see all available bots.

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
        
        # Send the reply
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=payload, timeout=10)
        print(f"Send message response: {response.status_code}")  # Log for debugging
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"Error in webhook: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run()
