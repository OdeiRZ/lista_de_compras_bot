import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token del bot
TOKEN = "8268360976:AAHXbvHk16UTcnsZs0XoeQlklrmX1j18674"

# Lista de la compra
SHOPPING_LIST = {
    "Lácteos": ["Leche", "Yogur", "Mantequilla"],
    "Huevos y derivados": ["Huevos", "Queso"],
    "Panadería": ["Pan", "Bollería"],
    "Frutas": ["Manzanas", "Plátanos", "Naranjas"],
    "Verduras": ["Tomate", "Lechuga", "Zanahoria"],
    "Otros": ["Aceite", "Azúcar", "Sal"]
}

# Estado inicial
state = {item: False for category in SHOPPING_LIST.values() for item in category}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostrar lista de la compra con botones."""
    keyboard = [
        [InlineKeyboardButton(f"{'✅' if state[item] else '⬜'} {item}", callback_data=item)]
        for category in SHOPPING_LIST.values() for item in category
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Lista de la compra:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Togglear estado del item."""
    query = update.callback_query
    await query.answer()

    item = query.data
    state[item] = not state[item]

    keyboard = [
        [InlineKeyboardButton(f"{'✅' if state[i] else '⬜'} {i}", callback_data=i)]
        for category in SHOPPING_LIST.values() for i in category
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Lista de la compra:", reply_markup=reply_markup)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resetear lista a todos sin marcar."""
    for item in state:
        state[item] = False

    keyboard = [
        [InlineKeyboardButton(f"⬜ {i}", callback_data=i)]
        for category in SHOPPING_LIST.values() for i in category
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Lista reseteada:", reply_markup=reply_markup)


def main():
    """Ejecutar bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CallbackQueryHandler(button))

    # Arrancar polling
    app.run_polling()


if __name__ == "__main__":
    main()
