from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

# ТВОЙ ТОКЕН
BOT_TOKEN = "8572689919:AAHYMpKOdp2ejZpq7n64mKOIIjDa2xTn-80"

# ТВОЙ USER ID
ALLOWED_USER_ID = 1346576926

# Данные в памяти (не сохраняются между перезапусками)
bot_data = {
    "mode": "Auto",
    "status": "РАБОТАЕТ",
    "coins": ["BTC", "ETH", "KAS"],
    "signals_today": 0,
    "signals_max": 15,
    "balance_start": 100.00,
    "balance_current": 100.00,
    "profit_pct": 0.0,
    "accuracy": 0,
    "risk_pct": 0
}

# Функция для генерации ASCII-бара
def make_bar(percentage, length=17):
    filled = int(percentage / 100 * length)
    return "█" * filled + "░" * (length - filled)

# Функция главного меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    # Обновляем данные
    today = datetime.now().strftime("%-d %B %Y")

    # Формируем сообщение
    message = (
        f"🌅 Доброе утро, {update.effective_user.first_name}!\n\n"
        f"📆 {today} | 🧪 Режим: ТЕСТ\n"
        f"🟢 Статус: {bot_data['status']} (сканирует каждые 30 сек)\n"
        f"🔄 В работе: 0 сделок\n"
        f"🌐 BTC: 📈 +0.5% | Доминирование: 51%\n\n"
        f"💰 Баланс: ${bot_data['balance_start']:.2f} → ${bot_data['balance_current']:.2f} ({bot_data['profit_pct']:+.1f}%)\n"
        f"🎯 Сигналов сегодня: {bot_data['signals_today']} из {bot_data['signals_max']}\n\n"
        f"📈 Прогресс дня:\n"
        f"| Профит  | {make_bar(bot_data['profit_pct'])} ({bot_data['profit_pct']:.0f}%) |\n"
        f"| Точность| {make_bar(bot_data['accuracy'])} ({bot_data['accuracy']:.0f}%) |\n"
        f"| Риск    | {make_bar(bot_data['risk_pct'])} ({bot_data['risk_pct']:.0f}%) |\n\n"
        f"👇 Что делаем?"
    )

    # Кнопки
    keyboard = [
        ["📊 Сигналы за сегодня", "📈 Статистика теста"],
        ["⚙️ Настройки", "📌 Мои монеты"],
        ["🔄 Обновить статус"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(message, reply_markup=reply_markup)

# Запуск бота
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
