from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
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

# Функция для команды /add
async def add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    if not context.args:
        await update.message.reply_text("❌ Укажи монету: /add KAS")
        return

    coin = context.args[0].upper()

    if coin in bot_data['coins']:
        await update.message.reply_text(f"✅ Монета {coin} уже в списке")
        return

    bot_data['coins'].append(coin)
    await update.message.reply_text(f"✅ Добавлена монета: {coin}")

# Функция для команды /remove
async def remove_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    if not context.args:
        await update.message.reply_text("❌ Укажи монету: /remove KAS")
        return

    coin = context.args[0].upper()

    if coin not in bot_data['coins']:
        await update.message.reply_text(f"❌ Монета {coin} не найдена в списке")
        return

    bot_data['coins'].remove(coin)
    await update.message.reply_text(f"✅ Удалена монета: {coin}")

# Функция для команды /coins
async def list_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    coins_list = "\n".join([f"• {coin} ✅" for coin in bot_data['coins']])
    message = f"📌 Мои монеты\n\nСейчас отслеживаю {len(bot_data['coins'])} монет:\n{coins_list}\n\n➕ Добавить новую монету: /add KAS"
    await update.message.reply_text(message)

# Функция для кнопки "Мои монеты"
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    text = update.message.text

    if text == "📌 Мои монеты":
        coins_list = "\n".join([f"• {coin} ✅" for coin in bot_data['coins']])
        message = f"📌 Мои монеты\n\nСейчас отслеживаю {len(bot_data['coins'])} монет:\n{coins_list}\n\n➕ Добавить новую монету: /add KAS"
        await update.message.reply_text(message)

# Запуск бота
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_coin))
    app.add_handler(CommandHandler("remove", remove_coin))
    app.add_handler(CommandHandler("coins", list_coins))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
