from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

# ТВОЙ ТОКЕН
BOT_TOKEN = "8572689919:AAHYMpKOdp2ejZpq7n64mKOIIjDa2xTn-80"

# ТВОЙ USER ID
ALLOWED_USER_ID = 1346576926

# Функция для генерации ASCII-бара
def make_bar(percentage, length=17):
    filled = int(percentage / 100 * length)
    return "█" * filled + "░" * (length - filled)

# Функция главного меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    # Данные для дашборда (временно статичные)
    today = datetime.now().strftime("%-d %B %Y")
    balance_start = 100.00
    balance_current = 100.00
    profit_pct = 0.0
    signals_done = 0
    signals_max = 15
    accuracy = 0
    risk_pct = 0

    # Формируем сообщение
    message = (
        f"🌅 Доброе утро, {update.effective_user.first_name}!\n\n"
        f"📆 {today} | 🧪 Режим: ТЕСТ\n"
        f"🟢 Статус: РАБОТАЕТ (сканирует каждые 30 сек)\n"
        f"🔄 В работе: 0 сделок\n"
        f"🌐 BTC: 📈 +0.5% | Доминирование: 51%\n\n"
        f"💰 Баланс: ${balance_start:.2f} → ${balance_current:.2f} ({profit_pct:+.1f}%)\n"
        f"🎯 Сигналов сегодня: {signals_done} из {signals_max}\n\n"
        f"📈 Прогресс дня:\n"
        f"| Профит  | {make_bar(profit_pct)} ({profit_pct:.0f}%) |\n"
        f"| Точность| {make_bar(accuracy)} ({accuracy:.0f}%) |\n"
        f"| Риск    | {make_bar(risk_pct)} ({risk_pct:.0f}%) |\n\n"
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
