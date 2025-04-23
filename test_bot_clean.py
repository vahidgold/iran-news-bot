import requests
from telegram.ext import Updater, CommandHandler

print("✅ ربات در حال اجراست...")

TOKEN = '7916933490:AAH_iK_3TFahvOhmr3zQPfJsYxkaQzuZBzg'
CHAT_ID = 98812350

def start(update, context):
    print("📩 دریافت دستور /start")
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ ربات به درستی در حال اجراست.")

def send_test_message():
    try:
        print("📤 در حال ارسال پیام تست به تلگرام...")
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": "🧪 پیام تست از ربات ساده‌شده"}
        )
        print("✅ پیام ارسال شد.")
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

send_test_message()

print("🚀 منتظر پیام‌های کاربر...")
updater.start_polling()
updater.idle()