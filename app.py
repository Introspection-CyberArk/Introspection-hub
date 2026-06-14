import os
import requests
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)

# ============ CONFIGURATION ============
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")  # Your hub bot token (create a NEW bot for this)

# ============ YOUR BOTS DATABASE ============
BOTS = [
    {
        "id": "jarvis",
        "name": "🤖 J.A.R.V.I.S. AI",
        "username": "@IntroAssit_Bot",
        "description": "Your personal AI assistant with voice recognition, weather updates, and smart conversations.",
        "features": [
            "🎤 Voice message support",
            "🌤️ Real-time weather updates",
            "💬 AI-powered conversations",
            "🕐 Current time & date",
            "🔍 Answers any question"
        ],
        "category": "AI Assistant",
        "status": "🟢 Active"
    },
    {
        "id": "currency",
        "name": "💱 Currency Exchange Bot",
        "username": "@currrency_exch_bot",
        "description": "Real-time currency exchange rates and conversion between 150+ currencies.",
        "features": [
            "💵 Live exchange rates",
            "🔄 Convert between currencies",
            "📊 Historical rate charts",
            "⭐ Save favorite pairs",
            "🌍 150+ currencies supported"
        ],
        "category": "Finance",
        "status": "🟢 Active"
    },
    {
        "id": "numspy",
        "name": "🔢 Num Spy Bot",
        "username": "@Num_Spy_Bot",
        "description": "Phone number lookup, caller ID, and number information tracker.",
        "features": [
            "📞 Phone number lookup",
            "📍 Country & operator info",
            "🕵️ Caller ID identification",
            "⚠️ Spam number detection",
            "📱 Carrier information"
        ],
        "category": "Utility",
        "status": "🟢 Active"
    }
]

# Group bots by category
CATEGORIES = {}
for bot in BOTS:
    cat = bot["category"]
    if cat not in CATEGORIES:
        CATEGORIES[cat] = []
    CATEGORIES[cat].append(bot)

# ============ COMMAND HANDLERS ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with bot hub menu"""
    keyboard = [
        [InlineKeyboardButton("📋 View All Bots", callback_data="list_all")],
        [InlineKeyboardButton("📂 Browse by Category", callback_data="categories")],
        [InlineKeyboardButton("👨‍💻 About Developer", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""🤖 **Welcome to @Introspection007's Bot Hub!**

I'm your central dashboard to access all my Telegram bots.

**{len(BOTS)} bots available** across multiple categories:
• 🤖 AI Assistant
• 💱 Finance
• 🔢 Utility

Use the buttons below to browse and launch any bot!

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = """🤖 **Bot Hub Help**

**How to use:**
1. Browse bots using the menu buttons
2. Click on any bot to see details
3. Click "Launch Bot" to open it

**Commands:**
/start - Show main menu
/help - Show this help
/bots - List all bots
/categories - Browse by category

**Need support?** Contact @Introspection007

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def bots_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all bots"""
    keyboard = []
    for bot in BOTS:
        keyboard.append([InlineKeyboardButton(f"{bot['name']} {bot['status']}", callback_data=f"bot_{bot['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🤖 **Available Bots ({len(BOTS)})**\n\nTap any bot to see details:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show categories"""
    keyboard = []
    for category in CATEGORIES.keys():
        count = len(CATEGORIES[category])
        keyboard.append([InlineKeyboardButton(f"📁 {category} ({count})", callback_data=f"cat_{category}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📂 **Browse by Category**\n\nSelect a category to see bots:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    stats_text = f"""📊 **Bot Hub Statistics**

📦 **Total Bots:** {len(BOTS)}
📂 **Categories:** {len(CATEGORIES)}

**By Category:**
"""
    for category, bots in CATEGORIES.items():
        stats_text += f"• {category}: {len(bots)} bots\n"
    
    stats_text += f"""
**Bot List:**
"""
    for bot in BOTS:
        stats_text += f"• {bot['name']} - {bot['status']}\n"
    
    stats_text += """
━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
    
    await update.message.reply_text(stats_text, parse_mode="Markdown")

# ============ CALLBACK HANDLERS ============

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "menu":
        keyboard = [
            [InlineKeyboardButton("📋 View All Bots", callback_data="list_all")],
            [InlineKeyboardButton("📂 Browse by Category", callback_data="categories")],
            [InlineKeyboardButton("👨‍💻 About Developer", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🤖 **Welcome back to Bot Hub!**\n\nSelect an option below:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif data == "list_all":
        keyboard = []
        for bot in BOTS:
            keyboard.append([InlineKeyboardButton(f"{bot['name']} {bot['status']}", callback_data=f"bot_{bot['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🤖 **All Bots ({len(BOTS)})**\n\nTap any bot for details:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif data == "categories":
        keyboard = []
        for category in CATEGORIES.keys():
            count = len(CATEGORIES[category])
            keyboard.append([InlineKeyboardButton(f"📁 {category} ({count})", callback_data=f"cat_{category}")])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📂 **Categories**\n\nSelect a category:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif data == "about":
        about_text = f"""👨‍💻 **About Bot Hub & Developer**

This hub was created by **@Introspection007** to provide easy access to all Telegram bots in one place.

**📦 Bots Available:** {len(BOTS)}
**📂 Categories:** {len(CATEGORIES)}

**🤖 My Bots:**
"""
        for bot in BOTS:
            about_text += f"• {bot['name']} - {bot['description'][:50]}...\n"
        
        about_text += """
**💡 Purpose:** Centralized access to all my bots

**🆓 All bots are FREE to use!**

For support, bugs, or suggestions:
Contact @Introspection007

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(about_text, reply_markup=reply_markup, parse_mode="Markdown")
    
    elif data.startswith("cat_"):
        category = data.replace("cat_", "")
        bots_in_cat = CATEGORIES.get(category, [])
        
        keyboard = []
        for bot in bots_in_cat:
            keyboard.append([InlineKeyboardButton(f"{bot['name']} {bot['status']}", callback_data=f"bot_{bot['id']}")])
        keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="categories")])
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📁 **{category}** ({len(bots_in_cat)} bots)\n\nSelect a bot:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    
    elif data.startswith("bot_"):
        bot_id = data.replace("bot_", "")
        bot = next((b for b in BOTS if b["id"] == bot_id), None)
        
        if bot:
            features_text = "\n".join([f"{f}" for f in bot["features"]])
            
            details_text = f"""🤖 **{bot['name']}** {bot['status']}

📝 **Description:**
{bot['description']}

✨ **Features:**
{features_text}

📌 **Username:** {bot['username']}
📂 **Category:** {bot['category']}

━━━━━━━━━━━━━━━━━━━━━
👨‍💻 **Powered By @Introspection007**"""
            
            keyboard = [
                [InlineKeyboardButton("🚀 Launch Bot", url=f"https://t.me/{bot['username'].replace('@', '')}")],
                [InlineKeyboardButton("🔙 Back to List", callback_data="list_all")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(details_text, reply_markup=reply_markup, parse_mode="Markdown")

# ============ FLASK WEBHOOK (for Vercel) ============

telegram_app = Application.builder().token(TOKEN).build()

# Register handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("bots", bots_command))
telegram_app.add_handler(CommandHandler("categories", categories_command))
telegram_app.add_handler(CommandHandler("stats", stats_command))
telegram_app.add_handler(CallbackQueryHandler(button_callback))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        await telegram_app.process_update(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "Bot Hub is running!",
        "creator": "@Introspection007",
        "bots_count": len(BOTS),
        "categories": len(CATEGORIES),
        "bots": [{"name": bot["name"], "username": bot["username"]} for bot in BOTS]
    })

if __name__ == "__main__":
    app.run()