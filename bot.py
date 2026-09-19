import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
GROUP_ID = os.getenv("GROUP_ID", "")

DEMO_NUMBERS = [
    "+880 17XX XXX 001",
    "+1 202 XXX 0002",
    "+44 7XXX XXX 003",
    "+91 98XX XXX 004",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Demo Numbers", callback_data="numbers")],
        [InlineKeyboardButton("🔐 Demo Verification", callback_data="verify")],
        [InlineKeyboardButton("📊 Status", callback_data="status")],
    ]
    await update.message.reply_text(
        "👑 RJ BOT MANAGEMENT\n\n"
        "🧪 DEMO / TEST MODE\n"
        "এই বট কোনো বাস্তব WhatsApp OTP সংগ্রহ বা লগইন করে না।\n\n"
        "নিচের মেনু ব্যবহার করুন:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Admin only.")
        return
    await update.message.reply_text(
        "🎛️ RJ ADMIN PANEL\n\n"
        "🟢 Bot: Online\n"
        "🧪 Mode: DEMO\n"
        "🔐 Real OTP capture: Disabled\n"
        "📢 Group notification: Demo only"
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "numbers":
        text = "📱 DEMO NUMBERS\n\n" + "\n".join(
            f"• {n} — 🧪 TEST ONLY" for n in DEMO_NUMBERS
        )
    elif q.data == "verify":
        text = (
            "🔐 DEMO VERIFICATION\n\n"
            "Number: +880 17XX XXX 001\n"
            "Status: ⏳ Waiting\n\n"
            "🧪 TEST OTP: 123456\n"
            "⚠️ This is a fictional test code. "
            "It cannot log into WhatsApp."
        )
    else:
        text = (
            "📊 SYSTEM STATUS\n\n"
            "🟢 Bot: Online\n"
            "🧪 Demo mode: Active\n"
            "🔒 Real OTP handling: Disabled"
        )

    await q.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
        ),
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start demo\n"
        "/panel - Admin panel\n"
        "/help - Help"
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(buttons))
    print("RJ Demo Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
