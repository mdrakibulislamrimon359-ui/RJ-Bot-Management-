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

COMMUNITY_NAME = "RJ Team Bangladesh Hekar Community"
BOT_NAME = "RJ Emotional AI"
OWNER_USERNAME = "@RJteam1"

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
        ],
        [
            InlineKeyboardButton(
                "👑 Owners",
                callback_data="owners"
            ),
            InlineKeyboardButton(
                "ℹ️ About",
                callback_data="about"
            )
        ],
        [
            InlineKeyboardButton(
                "🧹 Reset",
                callback_data="reset"
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
তুমি "{BOT_NAME}"-এর একজন
professional বাংলা content writer.

তুমি "{COMMUNITY_NAME}"-এর পক্ষ থেকে
ব্যবহারকারীর একজন বন্ধুর মতো কথা বলবে।

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

    # নতুন conversation state
    context.user_data.clear()

    text = (
        "🌹 <b>RJ Emotional AI</b>\n\n"

        "🤖 আমি আপনার AI Intelligent Friend।\n"
        "❤️ আমি <b>RJ Team Bangladesh Hekar Community</b>-এর "
        "পক্ষ থেকে আপনার বন্ধু হিসেবে থাকতে চাই।\n\n"

        "এক কথায়—<b>আমি আপনার বন্ধু।</b> 🤝\n\n"

        "আপনি আমাকে যেকোনো SMS বা বিষয় পাঠান।\n"
        "আপনার SMS-এর অর্থ ও অনুভূতির ওপর নির্ভর করে "
        "আমি সুন্দর emotional ও social-media friendly "
        "caption তৈরি করে দেব। 🌸\n\n"

        "🌸 Facebook Caption\n"
        "🎵 TikTok Caption\n"
        "#️⃣ Hashtags\n\n"

        "✍️ উদাহরণ:\n"
        "<i>কিছু মানুষ দূরে চলে গেলেও "
        "মনে থেকে যায়...</i>"
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
        "🆘 <b>RJ Emotional AI — Help</b>\n\n"

        "/start — 🤖 Bot শুরু করুন\n"
        "/help — 🆘 Help দেখুন\n"
        "/panel — ⚙️ Admin Panel\n"
        "/about — ℹ️ Bot সম্পর্কে জানুন\n"
        "/owners — 👑 Owner Information\n"
        "/reset — 🧹 নতুন করে SMS শুরু করুন\n\n"

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
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# ABOUT COMMAND
# =========================================================

async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🤖 <b>আমি RJ Emotional AI</b>\n\n"

        "🌹 আমি আপনার AI Intelligent Friend।\n\n"

        "<b>RJ Team Bangladesh Hekar Community</b>-এর "
        "পক্ষ থেকে আমি আপনার বন্ধু হিসেবে থাকতে চাই। ❤️\n\n"

        "এক কথায়—<b>আমি আপনার বন্ধু।</b> 🤝\n\n"

        "আপনি আমাকে যে SMS দেবেন, "
        "আপনার SMS-এর অর্থ ও অনুভূতির ওপর নির্ভর করে "
        "আমি সুন্দর, আবেগপূর্ণ ও মানানসই Caption তৈরি করে দেব। 💔🌹\n\n"

        "✨ আপনার অনুভূতি → আমার সুন্দর Caption\n\n"

        "🌸 Facebook Caption\n"
        "🎵 TikTok Caption\n"
        "#️⃣ Hashtags\n\n"

        "<b>RJ Emotional AI — আপনার অনুভূতির ডিজিটাল বন্ধু।</b> 🤖❤️"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================================================
# OWNERS COMMAND
# =========================================================

async def owners(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "👑 <b>RJ Team Information</b>\n\n"

        "🌹 <b>Community:</b>\n"
        "RJ Team Bangladesh Hekar Community\n\n"

        "👑 <b>Owner:</b> @RJteam1\n\n"

        "🤖 <b>Bot:</b> RJ Emotional AI\n\n"

        "📩 Owner-এর সাথে যোগাযোগ করতে নিচের "
        "button-এ চাপ দিন।"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "👑 Owner @RJteam1",
                url="https://t.me/RJteam1"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="home"
            )
        ]
    ]

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================================================
# RESET COMMAND
# =========================================================

async def reset(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    text = (
        "🧹 <b>Reset সম্পন্ন হয়েছে!</b>\n\n"

        "আগের conversation state পরিষ্কার করা হয়েছে।\n\n"

        "🤖 এখন থেকে আমরা নতুন করে SMS শুরু করতে পারি। ❤️\n\n"

        "✍️ আপনার নতুন SMS বা বিষয়টি পাঠান।\n"
        "আমি সেটার অনুভূতি বুঝে সুন্দর caption তৈরি করে দেব। 🌹"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
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
        "✅ Emotional Caption Active\n"
        "✅ Reset Command Active\n"
        "✅ Owners Command Active\n"
        "✅ About Command Active"
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
    # HOME
    # -----------------------------

    if query.data == "home":

        await query.message.reply_text(
            "🏠 <b>Main Menu</b>\n\n"
            "আপনার বিষয় বা SMS পাঠান। ❤️",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    # -----------------------------
    # RESET
    # -----------------------------

    if query.data == "reset":

        context.user_data.clear()

        await query.message.reply_text(
            "🧹 <b>Reset সম্পন্ন হয়েছে!</b>\n\n"
            "আগের conversation state পরিষ্কার হয়েছে।\n"
            "এখন নতুন করে SMS পাঠান। 🌹",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

    # -----------------------------
    # OWNERS
    # -----------------------------

    if query.data == "owners":

        keyboard = [
            [
                InlineKeyboardButton(
                    "👑 Owner @RJteam1",
                    url="https://t.me/RJteam1"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Main Menu",
                    callback_data="home"
                )
            ]
        ]

        await query.message.reply_text(
            "👑 <b>RJ Team Information</b>\n\n"
            "🌹 Community: "
            "<b>RJ Team Bangladesh Hekar Community</b>\n\n"
            "👑 Owner: @RJteam1\n\n"
            "নিচের button-এ চাপ দিলে Owner-এর Telegram profile-এ যাবে।",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # -----------------------------
    # ABOUT
    # -----------------------------

    if query.data == "about":

        await query.message.reply_text(
            "🤖 <b>আমি RJ Emotional AI</b>\n\n"
            "🌹 আমি আপনার AI Intelligent Friend।\n\n"
            "<b>RJ Team Bangladesh Hekar Community</b>-এর "
            "পক্ষ থেকে আমি আপনার বন্ধু হিসেবে থাকতে চাই। ❤️\n\n"
            "এক কথায়—<b>আমি আপনার বন্ধু।</b> 🤝\n\n"
            "আপনি আমাকে যে SMS দেবেন, "
            "আপনার SMS-এর অর্থ ও অনুভূতির ওপর নির্ভর করে "
            "আমি সুন্দর, আবেগপূর্ণ ও মানানসই Caption তৈরি করে দেব। 💔🌹\n\n"
            "✨ আপনার অনুভূতি → আমার সুন্দর Caption\n\n"
            "🌸 Facebook Caption\n"
            "🎵 TikTok Caption\n"
            "#️⃣ Hashtags\n\n"
            "<b>RJ Emotional AI — আপনার অনুভূতির ডিজিটাল বন্ধু।</b> 🤖❤️",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

        return

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
            f"👑 <b>RJ Team Admin Panel</b>\n\n"
            f"🟢 Status: Online\n"
            f"🤖 Model: <code>{MODEL}</code>\n"
            f"👤 Admin: @{ADMIN_USERNAME}",
            parse_mode="HTML"
        )

        return

    # -----------------------------
    # EMOTIONAL
    # -----------------------------

    if query.data == "emotional":

        await query.message.reply_text(
            "💔 <b>Emotional Caption</b>\n\n"
            "যে বিষয় নিয়ে emotional caption চান,\n"
            "সেটি লিখে পাঠান।\n\n"
            "উদাহরণ:\n"
            "কিছু মানুষ হারিয়ে গেলেও "
            "তাদের স্মৃতি থেকে যায়।",
            parse_mode="HTML"
        )

        return

    # -----------------------------
    # FACEBOOK
    # -----------------------------

    if query.data == "facebook":

        await query.message.reply_text(
            "📘 <b>Facebook Caption</b>\n\n"
            "আপনার বিষয় লিখে পাঠান।",
            parse_mode="HTML"
        )

        return

    # -----------------------------
    # TIKTOK
    # -----------------------------

    if query.data == "tiktok":

        await query.message.reply_text(
            "🎵 <b>TikTok Caption</b>\n\n"
            "আপনার বিষয় লিখে পাঠান।",
            parse_mode="HTML"
        )

        return


# =========================================================
# TEXT HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

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

    # =====================================================
    # COMMANDS
    # =====================================================

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

    application.add_handler(
        CommandHandler(
            "about",
            about
        )
    )

    application.add_handler(
        CommandHandler(
            "owners",
            owners
        )
    )

    application.add_handler(
        CommandHandler(
            "reset",
            reset
        )
    )

    # =====================================================
    # BUTTONS
    # =====================================================

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # =====================================================
    # NORMAL TEXT
    # =====================================================

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    # =====================================================
    # ERROR HANDLER
    # =====================================================

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "RJ Emotional AI started."
    )

    application.run_polling(
        drop_pending_updates=True
    )


# =========================================================
# START BOT
# =========================================================

if __name__ == "__main__":
    main()
