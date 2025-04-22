import requests
from googletrans import Translator
import pytz
from telegram.ext import Updater, CallbackContext, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import random

# 🔐 تنظیمات ربات
TOKEN = '7916933490:AAH_iK_3TFahvOhmr3zQPfJsYxkaQzuZBzg'
CHAT_ID = 98812350
NEWS_API_KEY = '64f57879182b4a85bbf39a55d7500e56'

# 🌐 مترجم
translator = Translator()

# 📥 دریافت خبر و ارسال به تلگرام
def auto_send_news(context: CallbackContext):
    bot = context.bot
    try:
        url = f'https://newsapi.org/v2/everything?q=iran&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])

        if not articles:
            bot.send_message(chat_id=CHAT_ID, text="❌ خبری پیدا نشد.")
            return

        article = random.choice(articles)
        title = article.get('title', 'بدون عنوان')
        description = article.get('description', 'بدون توضیح')
        link = article.get('url', '')

        # ترجمه
        translated_title = translator.translate(title, src='en', dest='fa').text
        translated_desc = translator.translate(description, src='en', dest='fa').text

        message = f"📰 *{translated_title}*\n\n{translated_desc}\n\n🔗 [مشاهده خبر]({link})"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown', disable_web_page_preview=False)

    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"⚠️ خطا در دریافت خبر:\n{e}")

# 🔘 دستور تست دستی
def start(update, context):
    update.message.reply_text("✅ ربات فعال است.")

# ⚙️ راه‌اندازی
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# ⏰ زمان‌بندی خودکار
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Tehran"))
scheduler.add_job(auto_send_news, 'interval', minutes=5, args=[updater.job_queue])
scheduler.start()

# ▶️ اجرای ربات
updater.start_polling()
updater.bot.send_message(chat_id=CHAT_ID, text="🤖 ربات با موفقیت راه‌اندازی شد!")
updater.idle()
