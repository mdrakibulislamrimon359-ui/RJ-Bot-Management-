# RJ Bot Management — Demo

এটি শুধুমাত্র UI/testing-এর জন্য একটি Telegram demo bot।

## নিরাপত্তা

- কোনো বাস্তব WhatsApp login নেই।
- কোনো আসল OTP সংগ্রহ/forward করা হয় না।
- দেখানো নম্বরগুলো fictional/demo placeholder।
- `123456` শুধুমাত্র test display code।

## Environment Variables

`BOT_TOKEN` = BotFather থেকে পাওয়া Telegram bot token  
`ADMIN_ID` = আপনার Telegram numeric user ID  
`GROUP_ID` = optional demo group ID

## Run

```bash
pip install -r requirements.txt
python bot.py
```

তারপর Telegram-এ `/start` পাঠান।
