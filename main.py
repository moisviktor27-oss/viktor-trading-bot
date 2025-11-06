from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ТВОЙ ТОКЕН
BOT_TOKEN = "8572689919:AAK_da3E1Q5GGR7eX0npANrq4c6uHCHL58"

# ТВОЙ USER ID
ALLOWED_USER_ID = 1346576926

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    await update.message.reply_text(
        f"🌅 Доброе утро, {update.effective_user.first_name}!\n\n"
        "Бот запущен и готов к работе 🟢\n"
        "Скоро здесь будет твой дашборд!"
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
