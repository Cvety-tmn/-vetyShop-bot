from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
TOKEN = os.getenv("BOT_TOKEN")
SITE_URL = "https://cvety-tmn.ru/"
PHONE = "+7 (919) 930-79-82"
BOT_NAME = "Цветы Событий"

KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🌐 Сайт", "📞 Позвонить"],
        ["ℹ️ О студии", "📍 Контакты"],
    ],
    resize_keyboard=True,
)

START_TEXT = (
    "Здравствуйте! 🌿\n"
    f"Добро пожаловать в «{BOT_NAME}».\n\n"
    "Я могу быстро показать сайт и контакты.\n"
    "Выберите нужный пункт в меню ниже."
)

ABOUT_TEXT = (
    "«Цветы Событий» — студия цветов и подарков.\n"
    "Здесь можно быстро перейти на сайт и связаться с нами по телефону."
)

CONTACT_TEXT = (
    f"Телефон: {PHONE}\n"
    f"Сайт: {SITE_URL}"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, reply_markup=KEYBOARD)

async def site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Наш сайт: {SITE_URL}",
        reply_markup=KEYBOARD,
        disable_web_page_preview=False
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTACT_TEXT, reply_markup=KEYBOARD)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ABOUT_TEXT, reply_markup=KEYBOARD)

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "🌐 Сайт":
        await site(update, context)
    elif text == "📞 Позвонить":
        await update.message.reply_text(f"Позвонить нам: {PHONE}", reply_markup=KEYBOARD)
    elif text == "ℹ️ О студии":
        await about(update, context)
    elif text == "📍 Контакты":
        await contact(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите кнопку в меню ниже.",
            reply_markup=KEYBOARD,
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("site", site))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    app.run_polling()

if __name__ == "__main__":
    main()
