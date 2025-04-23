import requests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from googletrans import Translator
import pytz
import random

TOKEN = "7916933490:AAH_iK_3TFahvOhmr3zQPfJsYxkaQzuZBzg"
CHAT_ID = 98812350
NEWS_API_KEY ='64f57879182b4a85bbf39a55d7500e56'
translator = Translator()

def send_news(context: CallbackContext, chat_id=CHAT_ID):
    try:
        url = f'https://newsapi.org/v2/everything?q=iran&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])
        if not articles:
            context.bot.send_message(chat_id=chat_id, text="❌ خبری پیدا نشد.")
            return

        article = random.choice(articles)
        title = translator.translate(article.get('title', ''), src='en', dest='fa').text
        desc = translator.translate(article.get('description', ''), src='en', dest='fa').text
        link = article.get('url', '')

        message = f"📰 *{title}*\n\n{desc}\n\n🔗 [مشاهده خبر]({link})"
        context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown', disable_web_page_preview=False)
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="⚠️ خطا در دریافت خبر.")

def get_top3_news(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        url = f'https://newsapi.org/v2/everything?q=iran&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])[:3]

        if not articles:
            update.message.reply_text("❌ خبری پیدا نشد.")
            return

        for article in articles:
            title = translator.translate(article.get('title', ''), src='en', dest='fa').text
            desc = translator.translate(article.get('description', ''), src='en', dest='fa').text
            link = article.get('url', '')
            message = f"📰 *{title}*\n\n{desc}\n\n🔗 [مشاهده خبر]({link})"
            context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown', disable_web_page_preview=False)
    except Exception as e:
        update.message.reply_text("⚠️ خطا در دریافت خبر.")

def start(update: Update, context: CallbackContext):
    keyboard = [['📰 خبر جدید', '📋 سه خبر مهم']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("سلام! یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=reply_markup)

def handle_text(update: Update, context: CallbackContext):
    text = update.message.text
    if text == '📰 خبر جدید':
        send_news(context, chat_id=update.effective_chat.id)
    elif text == '📋 سه خبر مهم':
        get_top3_news(update, context)

def scheduled_send(context: CallbackContext):
    send_news(context)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("news", lambda u, c: send_news(c, chat_id=u.effective_chat.id)))
dispatcher.add_handler(CommandHandler("top3", get_top3_news))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Tehran"))
scheduler.add_job(scheduled_send, 'interval', minutes=5, args=[updater.job_queue])
scheduler.start()

updater.start_polling()
updater.bot.send_message(chat_id=CHAT_ID, text="🤖 ربات با موفقیت راه‌اندازی شد!")
updater.idle()