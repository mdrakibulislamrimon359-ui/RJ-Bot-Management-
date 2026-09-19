import os
import asyncio
import logging

from google import genai

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)


# =========================================================
# CONFIGURATION
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

ADMIN_USERNAME = (
    os.getenv("ADMIN_USERNAME", "RJteam1")
    .strip()
    .lstrip("@")
    .lower()
)

# নতুন Gemini Model
MODEL = "gemini-3.5-flash-lite"


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("RJ-Team-AI-Bot")


# =========================================================
# CHECK ENVIRONMENT
# =========================================================

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing."
    )

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is missing."
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# MAIN KEYBOARD
# =========================================================

def main_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "💔 Emotional Caption",
                callback_data="emotional"
            )
        ],
        [
            InlineKeyboardButton(
                "📘 Facebook Caption",
                callback_data="facebook"
            ),
            InlineKeyboardButton(
                "🎵 TikTok Caption",
                callback_data="tiktok"
            )
        ],
        [
            InlineKeyboardButton(
                "⚙️ Admin Panel",
                callback_data="panel"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# ADMIN CHECK
# =========================================================

def is_admin(update: Update):

    user = update.effective_user

    if not user:
        return False

    username = (
        user.username or ""
    ).strip().lstrip("@").lower()

    return username == ADMIN_USERNAME


# =========================================================
# GEMINI PROMPT
# =========================================================

def create_prompt(topic):

    return f"""
তুমি "RJ Team AI Caption Studio"-এর একজন
professional বাংলা content writer.

ব্যবহারকারীর দেওয়া বিষয়:

{topic}

এই বিষয় অনুযায়ী সুন্দর, প্রাকৃতিক,
আবেগপূর্ণ এবং social-media friendly caption তৈরি করো।

ব্যবহারকারীর মূল অর্থ পরিবর্তন করবে না।
কোনো বানানো ঘটনা, নাম বা তথ্য যোগ করবে না।

নিচের format ঠিকভাবে অনুসরণ করো:

🌸 Facebook Caption:

একটি সুন্দর emotional এবং premium Facebook caption লিখবে।

🎵 TikTok Caption:

একটি ছোট, catchy এবং emotional TikTok caption লিখবে।

#️⃣ Hashtags:

বিষয়ের সাথে সম্পর্কিত 8 থেকে 12টি hashtag দেবে।

নিয়ম:

- বাংলা ভাষা ব্যবহার করবে।
- ভাষা সহজ ও সুন্দর হবে।
- প্রয়োজন অনুযায়ী emoji ব্যবহার করবে।
- অতিরিক্ত emoji ব্যবহার করবে না।
- প্রেমের বিষয় হলে romantic tone।
- কষ্টের বিষয় হলে emotional tone।
- পরিবার হলে heartfelt tone।
- বন্ধুত্ব হলে friendly tone।
- স্বপ্ন/সাফল্য হলে motivational tone।
- ব্যবসা হলে professional tone।
- কোনো মিথ্যা তথ্য তৈরি করবে না।
- কোনো code block ব্যবহার করবে না।
"""


# =========================================================
# ASK GEMINI
# =========================================================

async def ask_gemini(prompt):

    def generate():

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        return (
            response.text or ""
        ).strip()

    return await asyncio.to_thread(generate)


# =========================================================
# START COMMAND
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "👑 <b>RJ Team AI Caption Studio</b>\n\n"

        "🤖 আপনার একটি বিষয় বা ছোট একটি লাইন "
        "আমাকে পাঠান।\n\n"

        "আমি আপনার জন্য তৈরি করে দেব:\n\n"

        "🌸 Facebook Caption\n"
        "🎵 TikTok Caption\n"
        "#️⃣ Hashtags\n\n"

        "✍️ উদাহরণ:\n"
        "<i>কিছু মানুষ দূরে চলে গেলেও "
        "মনে থেকে যায়</i>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# HELP COMMAND
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🆘 <b>RJ Team Help</b>\n\n"

        "/start — Bot শুরু করুন\n"
        "/help — Help দেখুন\n"
        "/panel — Admin Panel\n\n"

        "📝 যেকোনো বিষয় লিখে পাঠান।\n"
        "AI আপনার জন্য সুন্দর caption তৈরি করবে।\n\n"

        "উদাহরণ:\n"
        "❤️ মায়ের ভালোবাসা\n"
        "💔 হারিয়ে যাওয়া মানুষ\n"
        "🤝 সত্যিকারের বন্ধুত্ব\n"
        "🔥 সফল হওয়ার স্বপ্ন"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


# =========================================================
# ADMIN PANEL
# =========================================================

async def panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_admin(update):

        await update.message.reply_text(
            "⛔ এই Panel শুধুমাত্র Admin-এর জন্য।"
        )

        return

    text = (
        "👑 <b>RJ Team Admin Panel</b>\n\n"

        "🟢 Bot Status: Online\n"
        f"🤖 AI Model: <code>{MODEL}</code>\n"
        f"👤 Admin: @{ADMIN_USERNAME}\n\n"

        "✅ Caption System Active\n"
        "✅ Facebook Caption Active\n"
        "✅ TikTok Caption Active\n"
        "✅ Emotional Caption Active"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # -----------------------------
    # ADMIN PANEL
    # -----------------------------

    if query.data == "panel":

        if not is_admin(update):

            await query.message.reply_text(
                "⛔ এই Panel শুধুমাত্র Admin-এর জন্য।"
            )

            return

        await query.message.reply_text(
            f"👑 RJ Team Admin Panel\n\n"
            f"🟢 Status: Online\n"
            f"🤖 Model: {MODEL}\n"
            f"👤 Admin: @{ADMIN_USERNAME}"
        )

        return

    # -----------------------------
    # EMOTIONAL
    # -----------------------------

    if query.data == "emotional":

        await query.message.reply_text(
            "💔 যে বিষয় নিয়ে emotional caption চান,\n"
            "সেটি লিখে পাঠান।\n\n"
            "উদাহরণ:\n"
            "কিছু মানুষ হারিয়ে গেলেও "
            "তাদের স্মৃতি থেকে যায়।"
        )

        return

    # -----------------------------
    # FACEBOOK
    # -----------------------------

    if query.data == "facebook":

        await query.message.reply_text(
            "📘 Facebook Caption-এর জন্য "
            "আপনার বিষয় লিখে পাঠান।"
        )

        return

    # -----------------------------
    # TIKTOK
    # -----------------------------

    if query.data == "tiktok":

        await query.message.reply_text(
            "🎵 TikTok Caption-এর জন্য "
            "আপনার বিষয় লিখে পাঠান।"
        )

        return


# =========================================================
# TEXT HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    topic = (
        update.message.text or ""
    ).strip()

    if not topic:
        return

    # Maximum input length
    if len(topic) > 2000:

        await update.message.reply_text(
            "⚠️ আপনার লেখা সর্বোচ্চ "
            "২০০০ অক্ষরের মধ্যে রাখুন।"
        )

        return

    waiting = await update.message.reply_text(
        "⏳ আপনার জন্য সুন্দর caption তৈরি করছি..."
    )

    try:

        prompt = create_prompt(topic)

        result = await ask_gemini(prompt)

        if not result:

            result = (
                "দুঃখিত, এই মুহূর্তে "
                "কোনো উত্তর পাওয়া যায়নি।"
            )

        await waiting.edit_text(result)

    except Exception as error:

        logger.exception(
            "Gemini API Error"
        )

        error_text = str(error)

        # 404 Model Error
        if (
            "404" in error_text
            or "NOT_FOUND" in error_text
        ):

            message = (
                "❌ Gemini Model পাওয়া যাচ্ছে না।\n\n"
                f"বর্তমান Model: {MODEL}\n\n"
                "Google AI Studio API access "
                "এবং API Key পরীক্ষা করুন।"
            )

        # API Key Error
        elif (
            "401" in error_text
            or "403" in error_text
        ):

            message = (
                "❌ Gemini API Key কাজ করছে না।\n\n"
                "Render-এর GEMINI_API_KEY "
                "সঠিকভাবে দেওয়া আছে কিনা পরীক্ষা করুন।"
            )

        # Quota / Rate Limit
        elif "429" in error_text:

            message = (
                "⏳ Gemini API quota বা rate limit "
                "পৌঁছে গেছে।\n\n"
                "কিছুক্ষণ পরে আবার চেষ্টা করুন।"
            )

        else:

            message = (
                "❌ AI থেকে caption নেওয়ার সময় "
                "একটি সমস্যা হয়েছে।\n\n"
                "Render Logs পরীক্ষা করুন।"
            )

        await waiting.edit_text(
            message
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update,
    context
):

    logger.error(
        "Unhandled error: %s",
        context.error
    )


# =========================================================
# MAIN
# =========================================================

def main():

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    application.add_handler(
        CommandHandler(
            "panel",
            panel
        )
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # Normal messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    # Error handler
    application.add_error_handler(
        error_handler
    )

    logger.info(
        "RJ Team AI Caption Studio started."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START BOT
# =========================================================

if __name__ == "__main__":
    main()
