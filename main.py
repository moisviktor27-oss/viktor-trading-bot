import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

# ТВОЙ ТОКЕН
BOT_TOKEN = "8572689919:AAHYMpKOdp2ejZpq7n64mKOIIjDa2xTn-80"

# ТВОЙ USER ID
ALLOWED_USER_ID = 1346576926

# Путь к файлам данных
DATA_DIR = "data"
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
COINS_FILE = os.path.join(DATA_DIR, "coins.json")

# Создаём папку data, если её нет
os.makedirs(DATA_DIR, exist_ok=True)

# Функция для загрузки данных
def load_data(file_path, default):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default

# Функция для сохранения данных
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Функция для генерации ASCII-бара
def make_bar(percentage, length=17):
    filled = int(percentage / 100 * length)
    return "█" * filled + "░" * (length - filled)

# Функция главного меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    # Загружаем настройки
    settings = load_data(SETTINGS_FILE, {
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
    })

    # Обновляем данные
    today = datetime.now().strftime("%-d %B %Y")

    # Формируем сообщение
    message = (
        f"🌅 Доброе утро, {update.effective_user.first_name}!\n\n"
        f"📆 {today} | 🧪 Режим: ТЕСТ\n"
        f"🟢 Статус: {settings['status']} (сканирует каждые 30 сек)\n"
        f"🔄 В работе: 0 сделок\n"
        f"🌐 BTC: 📈 +0.5% | Доминирование: 51%\n\n"
        f"💰 Баланс: ${settings['balance_start']:.2f} → ${settings['balance_current']:.2f} ({settings['profit_pct']:+.1f}%)\n"
        f"🎯 Сигналов сегодня: {settings['signals_today']} из {settings['signals_max']}\n\n"
        f"📈 Прогресс дня:\n"
        f"| Профит  | {make_bar(settings['profit_pct'])} ({settings['profit_pct']:.0f}%) |\n"
        f"| Точность| {make_bar(settings['accuracy'])} ({settings['accuracy']:.0f}%) |\n"
        f"| Риск    | {make_bar(settings['risk_pct'])} ({settings['risk_pct']:.0f}%) |\n\n"
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
    # Инициализируем данные
    if not os.path.exists(SETTINGS_FILE):
        save_data(SETTINGS_FILE, {
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
        })
    if not os.path.exists(COINS_FILE):
        save_data(COINS_FILE, ["BTC", "ETH", "KAS"])

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
