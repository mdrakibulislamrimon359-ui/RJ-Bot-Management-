import os
import logging

from google import genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================================================
# SETTINGS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "RJteam1").lstrip("@").lower()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing.")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing.")

# Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================================================
# AI PROMPT
# =========================================================

CAPTION_PROMPT = """
তুমি RJ Team-এর Premium AI Emotional Caption Writer।

ব্যবহারকারী যেকোনো একটি বিষয় খুব ছোট করে লিখবে।
তুমি সেই বিষয়কে সুন্দর, হৃদয়ছোঁয়া, আবেগপূর্ণ এবং
social-media friendly caption-এ রূপান্তর করবে।

দুটি আলাদা Caption তৈরি করবে:

1. Facebook Caption
2. TikTok Caption

নিয়ম:

• ব্যবহারকারীর মূল বক্তব্য ঠিক রাখবে।
• অযথা কোনো তথ্য বানাবে না।
• ভাষা হবে সুন্দর, প্রাকৃতিক ও আবেগপূর্ণ বাংলা।
• প্রয়োজন অনুযায়ী সুন্দর emoji ব্যবহার করবে।
• Facebook caption একটু বিস্তারিত হবে।
• TikTok caption ছোট, catchy এবং emotional হবে।
• প্রতিটির শেষে 5-10টি relevant hashtag দেবে।
• প্রেমের বিষয় হলে romantic emotional tone।
• কষ্টের বিষয় হলে deep emotional tone।
• মা/বাবা/পরিবার হলে হৃদয়ছোঁয়া tone।
• বন্ধুত্ব হলে warm friendship tone।
• সফলতা হলে inspirational tone।
• ব্যবসা/প্রমোশন হলে premium professional tone।
• একই caption বারবার ব্যবহার করবে না।
• কোনো fake claim, price, phone number বা link তৈরি করবে না।

OUTPUT FORMAT:

📘 FACEBOOK EMOTIONAL CAPTION

[Facebook caption]

🏷️ Hashtags:
[hashtags]


🎵 TIKTOK EMOTIONAL CAPTION

[TikTok caption]

🏷️ Hashtags:
[hashtags]
"""

# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("❤️ Emotional Caption", callback_data="emotional")
        ],
        [
            InlineKeyboardButton("📘 Facebook", callback_data="facebook"),
            InlineKeyboardButton("🎵 TikTok", callback_data="tiktok"),
        ],
        [
            InlineKeyboardButton("👑 Admin Panel", callback_data="admin"),
        ],
    ]

    await update.message.reply_text(
        "👑 RJ TEAM AI CAPTION STUDIO\n\n"
        "💎 Premium Emotional Caption Generator\n\n"
        "আপনি শুধু আপনার বিষয়টি ছোট করে লিখুন।\n"
        "আমি সেটাকে সুন্দর ও হৃদয়ছোঁয়া Caption বানিয়ে দেব। ❤️\n\n"
        "📘 Facebook Caption\n"
        "🎵 TikTok Caption\n"
        "🏷️ Smart Hashtags\n\n"
        "✍️ উদাহরণ:\n"
        "মা পাশে না থাকলে পৃথিবীটা অনেক ফাঁকা লাগে।",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# =========================================================
# HELP
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📝 RJ TEAM CAPTION HELP\n\n"
        "আপনার বিষয়টি ছোট করে লিখে Send করুন।\n\n"
        "❤️ Emotional\n"
        "💔 Sad\n"
        "💕 Love\n"
        "👩‍👦 Family\n"
        "🤝 Friendship\n"
        "🔥 Motivation\n"
        "💼 Business\n"
        "🚀 Promotion\n\n"
        "AI নিজে থেকে Facebook ও TikTok-এর জন্য সুন্দর Caption তৈরি করবে।"
    )

# =========================================================
# ADMIN PANEL
# =========================================================

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = (update.effective_user.username or "").lower()

    if username != ADMIN_USERNAME:
        await update.message.reply_text(
            "⛔ এই Admin Panel শুধুমাত্র Admin-এর জন্য।"
        )
        return

    await update.message.reply_text(
        "👑 RJ TEAM ADMIN PANEL\n\n"
        "🟢 Bot: ONLINE\n"
        "🤖 Gemini AI: ACTIVE\n"
        "❤️ Emotional Caption: ACTIVE\n"
        "📘 Facebook Mode: ACTIVE\n"
        "🎵 TikTok Mode: ACTIVE\n"
        "🔐 Admin: @" + ADMIN_USERNAME
    )

# =========================================================
# BUTTONS
# =========================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "emotional":

        await query.message.reply_text(
            "❤️ Emotional Caption Mode Active\n\n"
            "এখন আপনার বিষয়টি ছোট করে লিখুন।"
        )

    elif query.data == "facebook":

        await query.message.reply_text(
            "📘 Facebook Caption Mode\n\n"
            "আপনার বিষয়টি Send করুন।"
        )

    elif query.data == "tiktok":

        await query.message.reply_text(
            "🎵 TikTok Caption Mode\n\n"
            "আপনার বিষয়টি Send করুন।"
        )

    elif query.data == "admin":

        username = (query.from_user.username or "").lower()

        if username != ADMIN_USERNAME:
            await query.message.reply_text(
                "⛔ আপনি Admin নন।"
            )
            return

        await query.message.reply_text(
            "👑 ADMIN PANEL\n\n"
            "🟢 Bot Online\n"
            "🤖 Gemini AI Active\n"
            "❤️ Emotional Mode Active"
        )

# =========================================================
# GEMINI AI
# =========================================================

async def generate_caption(topic: str):

    prompt = CAPTION_PROMPT + "\n\nUSER TOPIC:\n" + topic

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )

    return response.text.strip()

# =========================================================
# MESSAGE HANDLER
# =========================================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    topic = (update.message.text or "").strip()

    if not topic:
        return

    waiting = await update.message.reply_text(
        "✍️ আপনার কথাটাকে সুন্দর করে সাজাচ্ছি...\n"
        "❤️ Emotional Caption তৈরি হচ্ছে..."
    )

    try:

        caption = await generate_caption(topic)

        await waiting.edit_text(caption)

    except Exception as error:

        logging.exception(
            "Gemini error: %s",
            error
        )

        await waiting.edit_text(
            "❌ Caption তৈরি করা যাচ্ছে না।\n\n"
            "GEMINI_API_KEY অথবা Gemini API status পরীক্ষা করুন।"
        )

# =========================================================
# MAIN
# =========================================================

def main():

    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("panel", panel)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("👑 RJ Team Gemini Caption Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
