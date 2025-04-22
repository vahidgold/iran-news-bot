import pytz
import time
from telegram.ext import Updater, CallbackContext, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# توکن و آیدی
TOKEN = '7916933490:AAH_iK_3TFahvOhmr3zQPfJsYxkaQzuZBzg'
CHAT_ID = 98812350

# تابع ارسال خودکار
def auto_send_news(context: CallbackContext):
    context.bot.send_message(chat_id=CHAT_ID, text="📢 خبر جدید درباره ایران")

# تابع تست دستی برای مطمئن شدن
def start(update, context):
    update.message.reply_text("✅ ربات با موفقیت اجرا شد.")

# ستاپ بات
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# فرمان /start
dispatcher.add_handler(CommandHandler("start", start))

# زمان‌بندی خودکار با pytz
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Tehran"))
scheduler.add_job(auto_send_news, 'interval', minutes=5, args=[updater.job_queue])
scheduler.start()

# راه‌اندازی ربات
updater.start_polling()
updater.bot.send_message(chat_id=CHAT_ID, text="🤖 ربات راه‌اندازی شد و در حال اجراست...")
updater.idle()
