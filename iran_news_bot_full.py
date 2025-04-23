import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
from googletrans import Translator
import pytz
import random

print("✅ ربات در حال اجراست...")

TOKEN = '7916933490:AAH_iK_3TFahvOhmr3zQPfJsYxkaQzuZBzg'
CHAT_ID = 98812350
NEWS_API_KEY = '64f57879182b4a85bbf39a55d7500e56'

translator = Translator()

# دریافت و ارسال یک خبر تصادفی
def send_news(context: CallbackContext, chat_id=CHAT_ID):
    print("🕓 دریافت خبر جدید...")
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
        print("❌ خطا:", e)
        context.bot.send_message(chat_id=chat_id, text="⚠️ خطا در دریافت خبر.")

# ارسال ۳ خبر با ترجمه
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
        print("❌ خطا در /top3:", e)
        update.message.reply_text("⚠️ خطا در دریافت خبر.")

# دکمه‌ها
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📰 یک خبر جدید", callback_data='news')],
        [InlineKeyboardButton("📋 سه خبر مهم", callback_data='top3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("سلام! یه گزینه رو انتخاب کن:", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'news':
        send_news(context, chat_id=query.message.chat.id)
    elif query.data == 'top3':
        get_top3_news(query, context)

# زمان‌بندی ارسال خودکار
def scheduled_send(context: CallbackContext):
    send_news(context)

# تنظیمات ربات
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("news", lambda u, c: send_news(c, chat_id=u.effective_chat.id)))
dispatcher.add_handler(CommandHandler("top3", get_top3_news))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

# Scheduler فعال
scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Tehran"))
scheduler.add_job(scheduled_send, 'interval', minutes=5, args=[updater.job_queue])
scheduler.start()

updater.start_polling()
print("🚀 ربات آماده دریافت دستورهاست.")
updater.bot.send_message(chat_id=CHAT_ID, text="🤖 ربات با موفقیت راه‌اندازی شد!")
updater.idle()