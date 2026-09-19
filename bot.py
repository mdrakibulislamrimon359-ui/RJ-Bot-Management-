import os
import logging
from openai import AsyncOpenAI

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# SETTINGS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "RJteam1").lstrip("@").lower()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing.")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing.")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================================================
# AI PROMPT
# =========================================================

CAPTION_PROMPT = """
তুমি RJ Team-এর একজন Premium Emotional Social Media Caption Writer।

ব্যবহারকারী খুব ছোট করে কোনো বিষয়, ঘটনা, অনুভূতি, সম্পর্ক,
স্মৃতি, ভালোবাসা, কষ্ট, সাফল্য, ব্যর্থতা, বন্ধুত্ব, পরিবার,
ব্যবসা, জীবন, স্বপ্ন বা যেকোনো সাধারণ বিষয় লিখবে।

তোমার কাজ হলো সেই ছোট কথাটাকে সুন্দর, হৃদয়ছোঁয়া এবং
emotionally engaging social-media caption-এ রূপান্তর করা।

নিয়ম:

1. ব্যবহারকারীর মূল অর্থ পরিবর্তন করবে না।
2. অযথা কোনো তথ্য, নাম, ঘটনা, টাকা, ফোন নম্বর বা দাবি বানাবে না।
3. ভাষা হবে প্রাকৃতিক, সুন্দর ও আবেগপূর্ণ বাংলা।
4. প্রয়োজন অনুযায়ী সুন্দর emoji ব্যবহার করবে।
5. Caption যেন কপি-পেস্ট করে Facebook/TikTok-এ ব্যবহার করা যায়।
6. Facebook caption একটু বিস্তারিত ও গল্পের মতো হবে।
7. TikTok caption ছোট, powerful এবং emotional হবে।
8. প্রতিটি caption-এর শেষে relevant hashtag দেবে।
9. অতিরিক্ত emoji বা অতিরঞ্জিত ভাষা ব্যবহার করবে না।
10. বিষয় যদি প্রেমের হয়, romantic/emotional tone ব্যবহার করবে।
11. বিষয় যদি কষ্টের হয়, sad/deep emotional tone ব্যবহার করবে।
12. বিষয় যদি সফলতার হয়, inspirational/emotional tone ব্যবহার করবে।
13. বিষয় যদি পরিবার/মায়ের হয়, warm এবং হৃদয়ছোঁয়া tone ব্যবহার করবে।
14. বিষয় যদি বন্ধুত্বের হয়, friendship/emotional tone ব্যবহার করবে।
15. বিষয় যদি ব্যবসা বা RJ Team সম্পর্কিত হয়, premium professional tone রাখবে।

OUTPUT FORMAT:

📘 FACEBOOK EMOTIONAL CAPTION

[সুন্দর Facebook caption]

🏷️ Hashtags:
[Relevant hashtags]


🎵 TIKTOK EMOTIONAL CAPTION

[ছোট কিন্তু শক্তিশালী TikTok caption]

🏷️ Hashtags:
[Relevant hashtags]
"""

# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👑 RJ TEAM EMOTIONAL CAPTION STUDIO\n\n"
        "💎 Premium AI Caption Generator\n\n"
        "আপনি শুধু আপনার মনের কথা বা বিষয়টি ছোট করে লিখুন।\n"
        "আমি সেটাকে সুন্দর, আবেগপূর্ণ ও হৃদয়ছোঁয়া Caption-এ "
        "রূপান্তর করে দেব। ❤️\n\n"
        "📘 Facebook Emotional Caption\n"
        "🎵 TikTok Emotional Caption\n"
        "🏷️ Relevant Hashtags\n\n"
        "✍️ উদাহরণ:\n"
        "“মাকে হারানোর পর বুঝেছি, পৃথিবীতে মায়ের মতো আপন কেউ নেই।”\n\n"
        "তারপর শুধু Send করুন। ❤️"
    )

    await update.message.reply_text(text)


# =========================================================
# HELP
# =========================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📝 RJ TEAM CAPTION HELP\n\n"
        "আপনার বিষয়টি ছোট করে লিখে Send করুন।\n\n"
        "❤️ প্রেম / অনুভূতি\n"
        "💔 কষ্ট / বিচ্ছেদ\n"
        "👩‍👦 মা / পরিবার\n"
        "🤝 বন্ধুত্ব\n"
        "🌱 জীবন / বাস্তবতা\n"
        "🔥 Motivation\n"
        "💼 Business / Promotion\n"
        "🚀 RJ Team / Website\n\n"
        "বট নিজে থেকে Facebook ও TikTok-এর জন্য আলাদা Caption তৈরি করবে।"
    )


# =========================================================
# ADMIN PANEL
# =========================================================

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = (update.effective_user.username or "").lower()

    if username != ADMIN_USERNAME:
        await update.message.reply_text(
            "⛔ এই Admin Panel শুধুমাত্র অনুমোদিত Admin-এর জন্য।"
        )
        return

    await update.message.reply_text(
        "👑 RJ TEAM ADMIN PANEL\n\n"
        "🟢 Bot Status: ONLINE\n"
        "🤖 AI Caption: ACTIVE\n"
        "❤️ Emotional Mode: ACTIVE\n"
        "📘 Facebook Mode: ACTIVE\n"
        "🎵 TikTok Mode: ACTIVE\n"
        "🔐 Admin: @" + ADMIN_USERNAME
    )


# =========================================================
# AI CAPTION GENERATOR
# =========================================================

async def generate_caption(topic: str) -> str:

    response = await client.responses.create(
        model="gpt-5-mini",
        instructions=CAPTION_PROMPT,
        input=topic,
    )

    return response.output_text.strip()


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
        "❤️ আপনার কথাটাকে সুন্দর করে সাজাচ্ছি...\n"
        "✍️ Emotional Caption তৈরি হচ্ছে..."
    )

    try:

        caption = await generate_caption(topic)

        await waiting.edit_text(caption)

    except Exception as error:

        logging.exception(
            "Caption generation error: %s",
            error
        )

        await waiting.edit_text(
            "❌ Caption তৈরি করা সম্ভব হচ্ছে না।\n\n"
            "দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।"
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
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("👑 RJ Team Emotional Caption Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
