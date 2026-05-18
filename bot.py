import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = 5759360747

BOT_NAME = "Цветы Событий Shop"
PHONE = "+7 (919) 930-79-82"
SITE_URL = "https://cvety-tmn.ru/"
ADDRESS = "Тюмень, Сакко 30/1"
WORK_TIME = "Ежедневно с 8:00 до 22:00"

CHOOSING, BUDGET, NAME, CONTACT, DELIVERY, COMMENT = range(6)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["💐 Подобрать букет", "ℹ️ О студии"],
        ["📍 Контакты", "👩‍💼 Связаться с менеджером"],
        ["🌐 Сайт", "🚚 Доставка"],
    ],
    resize_keyboard=True,
)

CONTACT_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📱 Отправить номер телефона", request_contact=True)],
        ["⬅️ Отмена"],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

START_TEXT = (
    "Здравствуйте! 🌿 \n"
    f"Добро пожаловать в «{BOT_NAME}».\n\n"
    "Я помогу подобрать букет, расскажу о доставке и быстро передам вашу заявку.\n"
    "Выберите нужный пункт в меню ниже."
)

ABOUT_TEXT = (
    "«Цветы Событий» — студия цветов и подарков.\n\n"
    f"📍 Адрес: {ADDRESS}\n"
    f"🕗 Режим работы: {WORK_TIME}\n"
    f"📞 Телефон: {PHONE}\n\n"
    "🚚 Доставка бесплатно в пределах окружной автодороги от 3000 руб.\n"
    "⏱ Доставка от 90 минут.\n"
    "🌿 Гарантия свежести — 48 часов."
)

CONTACT_TEXT = (
    f"📍 Адрес: {ADDRESS}\n"
    f"🕗 Режим работы: {WORK_TIME}\n"
    f"📞 Телефон: {PHONE}\n"
    f"🌐 Сайт: {SITE_URL}"
)

DELIVERY_TEXT = (
    "🚚 Условия доставки:\n\n"
    "• Бесплатно в пределах окружной автодороги при заказе от 3000 руб.\n"
    "• Доставка от 90 минут.\n"
    "• Гарантия свежести — 48 часов."
)

MANAGER_TEXT = (
    f"Связаться с менеджером:\n{PHONE}\n\n"
    "Или оставьте заявку через кнопку «💐 Подобрать букет», и мы напишем вам сами."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, reply_markup=MAIN_KEYBOARD)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ABOUT_TEXT, reply_markup=MAIN_KEYBOARD)

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTACT_TEXT, reply_markup=MAIN_KEYBOARD)

async def delivery_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DELIVERY_TEXT, reply_markup=MAIN_KEYBOARD)

async def site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🌐 Наш сайт: {SITE_URL}",
        reply_markup=MAIN_KEYBOARD,
        disable_web_page_preview=False,
    )

async def manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MANAGER_TEXT, reply_markup=MAIN_KEYBOARD)

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Для какого повода нужен букет?\n"
        "Например: день рождения, свадьба, благодарность, без повода.",
        reply_markup=ReplyKeyboardMarkup([["⬅️ Отмена"]], resize_keyboard=True),
    )
    return CHOOSING

async def order_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "⬅️ Отмена":
        await update.message.reply_text("Заявка отменена.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    context.user_data["reason"] = text
    await update.message.reply_text(
        "На какой бюджет ориентируемся?\n"
        "Например: до 3000, 3000–5000, 5000+"
    )
    return BUDGET

async def order_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "⬅️ Отмена":
        await update.message.reply_text("Заявка отменена.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    context.user_data["budget"] = text
    await update.message.reply_text("Как вас зовут?")
    return NAME

async def order_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "⬅️ Отмена":
        await update.message.reply_text("Заявка отменена.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    context.user_data["name"] = text
    await update.message.reply_text(
        "Отправьте номер телефона кнопкой ниже или напишите его сообщением.",
        reply_markup=CONTACT_KEYBOARD,
    )
    return CONTACT

async def order_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.strip() == "⬅️ Отмена":
        await update.message.reply_text("Заявка отменена.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    phone = ""
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = (update.message.text or "").strip()

    context.user_data["phone"] = phone

    await update.message.reply_text(
        "Укажите адрес доставки или напишите «Самовывоз».",
        reply_markup=ReplyKeyboardMarkup([["Самовывоз"], ["⬅️ Отмена"]], resize_keyboard=True),
    )
    return DELIVERY

async def order_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "⬅️ Отмена":
        await update.message.reply_text("Заявка отменена.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    context.user_data["delivery"] = text
    await update.message.reply_text(
        "Добавьте комментарий к заказу:\n"
        "например, дата, время, пожелания по цветам.\n\n"
        "Если комментария нет — напишите «Нет»."
    )
    return COMMENT

async def order_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "⬅️ Отмена":
        await update.message.reply_text("Заявка отменена.", reply_markup=MAIN_KEYBOARD)
        return ConversationHandler.END

    context.user_data["comment"] = text

    user = update.effective_user
    username = f"@{user.username}" if user.username else "без username"

    admin_text = (
        "📩 Новая заявка из бота\n\n"
        f"Имя: {context.user_data.get('name', '-')}\n"
        f"Телефон: {context.user_data.get('phone', '-')}\n"
        f"Повод: {context.user_data.get('reason', '-')}\n"
        f"Бюджет: {context.user_data.get('budget', '-')}\n"
        f"Доставка: {context.user_data.get('delivery', '-')}\n"
        f"Комментарий: {context.user_data.get('comment', '-')}\n\n"
        f"Username: {username}\n"
        f"User ID: {user.id}\n"
        f"Chat ID: {update.effective_chat.id}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text)
    except Exception:
        pass

    await update.message.reply_text(
        "Спасибо! 🌸\n"
        "Заявка отправлена. Мы свяжемся с вами в ближайшее время для подтверждения заказа.",
        reply_markup=MAIN_KEYBOARD,
    )

    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Действие отменено.", reply_markup=MAIN_KEYBOARD)
    return ConversationHandler.END

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    if text == "💐 Подобрать букет":
        return await order_start(update, context)
    elif text == "ℹ️ О студии":
        await about(update, context)
    elif text == "📍 Контакты":
        await contacts(update, context)
    elif text == "👩‍💼 Связаться с менеджером":
        await manager(update, context)
    elif text == "🌐 Сайт":
        await site(update, context)
    elif text == "🚚 Доставка":
        await delivery_info(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите нужную кнопку в меню ниже.",
            reply_markup=MAIN_KEYBOARD,
        )

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("order", order_start),
            MessageHandler(filters.Regex("^💐 Подобрать букет$"), order_start),
        ],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_reason)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_budget)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_name)],
            CONTACT: [
                MessageHandler(filters.CONTACT, order_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, order_contact),
            ],
            DELIVERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_delivery)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("contact", contacts))
    app.add_handler(CommandHandler("site", site))
    app.add_handler(CommandHandler("delivery", delivery_info))
    app.add_handler(CommandHandler("manager", manager))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    app.run_polling()

if __name__ == "__main__":
    main()

