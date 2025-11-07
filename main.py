from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime
import json
import os
import logging

# Включаем логирование для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ТВОЙ ТОКЕН
BOT_TOKEN = "8572689919:AAHYMpKOdp2ejZpq7n64mKOIIjDa2xTn-80"

# ТВОЙ USER ID
ALLOWED_USER_ID = 1346576926

# Данные в памяти
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
    logger.info(f"User {update.effective_user.id} started the bot")
    
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("❌ Доступ запрещен")
        return

    now = datetime.now()
    today = now.strftime("%-d %B %Y, %H:%M:%S")

    message = (
        f"💰💰 BYBIT Dashboard | {update.effective_user.first_name}\n\n"
        f"⏰ {today} | 🧪 ТЕСТ\n"
        f"🟢 Статус: {bot_data['status']} (сканирует каждые 30 сек)\n"
        f"🔄 В работе: 0 сделок\n"
        f"🌐 BTC: 📈 +0.5% | Доминирование: 51%\n\n"
        f"💲💲 Баланс: ${bot_data['balance_start']:.2f} → ${bot_data['balance_current']:.2f} ({bot_data['profit_pct']:+.1f}%)\n"
        f"🎯 Сигналов сегодня: {bot_data['signals_today']} из {bot_data['signals_max']}\n\n"
        f"📈 Прогресс дня:\n"
        f"| Профит  | {make_bar(bot_data['profit_pct'])} ({bot_data['profit_pct']:.0f}%) |\n"
        f"| Точность| {make_bar(bot_data['accuracy'])} ({bot_data['accuracy']:.0f}%) |\n"
        f"| Риск    | {make_bar(bot_data['risk_pct'])} ({bot_data['risk_pct']:.0f}%) |\n\n"
    )

    keyboard = [
        ["📊 Сигналы за сегодня", "📈 Статистика теста"],
        ["⚙️ Настройки", "📌 Мои монеты"],
        ["🔄 Обновить статус"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(message, reply_markup=reply_markup)

# Простая команда для проверки
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Ping from user {update.effective_user.id}")
    
    if update.effective_user.id != ALLOWED_USER_ID:
        return
        
    current_time = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"🟢 Бот жив! Время: {current_time}")

# Команда для добавления монеты
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

# Команда для удаления монеты  
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

# Команда для списка монет
async def list_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    coins_list = "\n".join([f"• {coin} ✅" for coin in bot_data['coins']])
    message = f"📌 Мои монеты\n\nСейчас отслеживаю {len(bot_data['coins'])} монет:\n{coins_list}\n\n➕ Добавить новую монету: /add KAS"
    await update.message.reply_text(message)

# Обработчик текстовых сообщений (кнопки)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    text = update.message.text
    logger.info(f"Received text: {text}")

    if text == "📌 Мои монеты":
        coins_list = "\n".join([f"• {coin} ✅" for coin in bot_data['coins']])
        message = f"📌 Мои монеты\n\nСейчас отслеживаю {len(bot_data['coins'])} монет:\n{coins_list}"
        
        keyboard = [
            [InlineKeyboardButton("➕ Добавить", callback_data="add_coin")],
            [InlineKeyboardButton("➖ Удалить", callback_data="remove_coin")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)

    elif text == "⚙️ Настройки":
        keyboard = [
            [InlineKeyboardButton(f"🔄 Режим: {bot_data['mode']}", callback_data="change_mode")],
            [InlineKeyboardButton(f"⏸️ Статус: {bot_data['status']}", callback_data="toggle_pause")],
            [InlineKeyboardButton(f"📊 Лимит: {bot_data['signals_max']}", callback_data="change_limit")],
            [InlineKeyboardButton("❌ Закрыть", callback_data="close_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = f"⚙️ Настройки\n\n🔹 Режим: {bot_data['mode']}\n🔹 Статус: {bot_data['status']}\n🔹 Лимит: {bot_data['signals_max']}"
        await update.message.reply_text(message, reply_markup=reply_markup)

    elif text == "🔄 Обновить статус":
        now = datetime.now()
        today = now.strftime("%-d %B %Y, %H:%M:%S")

        message = (
            f"💰💰 BYBIT Dashboard | {update.effective_user.first_name}\n\n"
            f"⏰ {today} | 🧪 ТЕСТ\n"
            f"🟢 Статус: {bot_data['status']}\n"
            f"🔄 В работе: 0 сделок\n\n"
            f"💲💲 Баланс: ${bot_data['balance_start']:.2f} → ${bot_data['balance_current']:.2f}\n"
            f"🎯 Сигналов: {bot_data['signals_today']} из {bot_data['signals_max']}"
        )

        keyboard = [
            ["📊 Сигналы за сегодня", "📈 Статистика теста"],
            ["⚙️ Настройки", "📌 Мои монеты"],
            ["🔄 Обновить статус"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(message, reply_markup=reply_markup)

# Обработчик inline-кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Button pressed: {query.data}")

    if query.data == "change_mode":
        keyboard = [
            [InlineKeyboardButton("Auto", callback_data="mode_Auto")],
            [InlineKeyboardButton("Swing", callback_data="mode_Swing")],
            [InlineKeyboardButton("Breakout", callback_data="mode_Breakout")],
            [InlineKeyboardButton("RSI", callback_data="mode_RSI")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🔄 Выбери режим анализа:", reply_markup=reply_markup)

    elif query.data.startswith("mode_"):
        mode = query.data.split("_")[1]
        bot_data['mode'] = mode
        await query.edit_message_text(f"✅ Режим изменён: {mode}")

    elif query.data == "toggle_pause":
        if bot_data['status'] == "РАБОТАЕТ":
            bot_data['status'] = "ПАУЗА"
            status_text = "⏸️ Бот поставлен на паузу"
        else:
            bot_data['status'] = "РАБОТАЕТ"
            status_text = "▶️ Бот возобновил работу"
        await query.edit_message_text(status_text)

    elif query.data == "change_limit":
        keyboard = [
            [InlineKeyboardButton("10", callback_data="limit_10")],
            [InlineKeyboardButton("15", callback_data="limit_15")],
            [InlineKeyboardButton("20", callback_data="limit_20")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📊 Выбери лимит сигналов:", reply_markup=reply_markup)

    elif query.data.startswith("limit_"):
        limit = int(query.data.split("_")[1])
        bot_data['signals_max'] = limit
        await query.edit_message_text(f"✅ Лимит изменён: {limit}")

    elif query.data == "close_settings":
        await query.edit_message_text("⚙️ Настройки закрыты")

    elif query.data == "add_coin":
        await query.edit_message_text("➕ Введите монету для добавления (например: KAS)")
        context.user_data['awaiting_add'] = True

    elif query.data == "remove_coin":
        await query.edit_message_text("➖ Введите монету для удаления (например: KAS)")
        context.user_data['awaiting_remove'] = True

# Обработчик ввода монет
async def handle_coin_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    text = update.message.text

    if context.user_data.get('awaiting_add'):
        coin = text.upper()
        if coin in bot_data['coins']:
            await update.message.reply_text(f"✅ Монета {coin} уже в списке")
        else:
            bot_data['coins'].append(coin)
            await update.message.reply_text(f"✅ Добавлена монета: {coin}")
        context.user_data.pop('awaiting_add', None)

    elif context.user_data.get('awaiting_remove'):
        coin = text.upper()
        if coin not in bot_data['coins']:
            await update.message.reply_text(f"❌ Монета {coin} не найдена в списке")
        else:
            bot_data['coins'].remove(coin)
            await update.message.reply_text(f"✅ Удалена монета: {coin}")
        context.user_data.pop('awaiting_remove', None)

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}")

# Главная функция
def main():
    print("🚀 Запускаю бота...")
    
    try:
        # Создаем приложение
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ping", ping))
        app.add_handler(CommandHandler("add", add_coin))
        app.add_handler(CommandHandler("remove", remove_coin))
        app.add_handler(CommandHandler("coins", list_coins))
        
        app.add_handler(CallbackQueryHandler(button_handler))
        
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_coin_input))
        
        app.add_error_handler(error_handler)
        
        # Запускаем бота
        print("🟢 Бот запущен!")
        print("📱 Открой Telegram и напиши /start")
        app.run_polling()
        
    except Exception as e:
        print(f"🔴 Ошибка запуска: {e}")
        print("Проверь токен и интернет-соединение")

if __name__ == "__main__":
    main()
