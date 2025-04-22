import requests
from googletrans import Translator
import pytz
from telegram.ext import Updater, CallbackContext, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import random

# تنظیمات کلید و اطلاعات ربات
TOKEN = '7916933490:AAH_iK_3TFahvOhmr3zQPfJsYxkaQzuZBzg'
CHAT_ID = 98812350
NEWS_API_KEY = '64f57879182b4a85bbf39a55d7500e56'

# مترجم گوگل
translator = Translator()

# ارسال خودکار هر 5 دقیقه
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

        translated_title = translator.translate(title, src='en', dest='fa').text
        translated_desc = translator.translate(description, src='en', dest='fa').text

        message = f"📰 *{translated_title}*\n\n{translated_desc}\n\n🔗 [مشاهده خبر]({link})"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown', disable_web_page_preview=False)

    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"⚠️ خطا در دریافت خبر:\n{e}")

# دستور دستی: /news
def get_news(update, context):
    auto_send_news(context)

# دستور دستی: /top3
def get_top3_news(update, context):
    try:
        url = f'https://newsapi.org/v2/everything?q=iran&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])[:3]

        if not articles:
            update.message.reply_text("❌ خبری پیدا نشد.")
            return

        for article in articles:
            title = article.get('title', 'بدون عنوان')
            description = article.get('description', 'بدون توضیح')
            link = article.get('url', '')

            translated_title = translator.translate(title, src='en', dest='fa').text
            translated_desc = translator.translate(description, src='en', dest='fa').text

            message = f"📰 *{translated_title}*\n\n{translated_desc}\n\n🔗 [مشاهده خبر]({link})"
            update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=False)

    except Exception as e:
        update.message.reply_text(f"⚠️ خطا در دریافت خبر:\n{e}")

# دستور start برای تست
def start(update, context):
    update.message.reply_text("✅ ربات فعال است.")

# ستاپ ربات
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("news", get_news))
dispatcher.add_handler(CommandHandler("top3", get_top3_news))

# زمان‌بندی خودکار هر ۵ دقیقه
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Tehran"))
scheduler.add_job(auto_send_news, 'interval', minutes=5, args=[updater.job_queue])
scheduler.start()

# اجرای ربات
updater.start_polling()
updater.bot.send_message(chat_id=CHAT_ID, text="🤖 ربات با موفقیت راه‌اندازی شد!")
updater.idle()