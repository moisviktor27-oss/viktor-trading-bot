from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, ContextTypes

# ТВОЙ ТОКЕН
BOT_TOKEN = "8572689919:AAHYMpKOdp2ejZpq7n64mKOIIjDa2xTn-80"

# ТВОЙ USER ID
ALLOWED_USER_ID = 1346576926

# Обработчик нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "add_coin":
        await query.edit_message_text("➕ Введите монету для добавления (например: KAS)")

# Запуск бота
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
