import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIG
# =========================

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    print("Error: define la variable de entorno TOKEN")
    exit(1)

STATE_FILE = "state.json"

# Lista inicial (si no existe state.json)
default_checklist = {
    "MERCADONA": [
		"Arena aglomerante", "Papel higiénico", "Toallitas culo", "Bolsas de basura", "Lavavajillas", "Pato WC", 
		"Nidos de pasta (al huevo)", "Hélices de pasta", 
		"Lágrima artificial", "Bastoncillos", "Enjuague bucal", "Pasta de dientes", 
		"Filetes de pavo", "Jamón extrafino", "Jamón ibérico", "Bacon", "Chorizo de pavo", "Pavo", "Queso mozarella", "Queso mozarella light", "Queso tierno", "Queso cuña",
		"Plátanos", "Manzanas", "Patatas", "Pimiento verde", "Zanahorias", "Guacamole", 
		"Chocolate Nestlé", "Helados de cono grandes", "Helados de cono chicos", 
		"Patatas gajo", "Patatas corte grueso", "Batatas congeladas", "Ñoquis congelados", "Pimiento congelado", "Cebolla congelada", "Ajo congelado",
		"Agua", "Monster", "Coca-cola zero", "Mosto tinto",
		"Salsa barbacoa", "Salsa de soja", "Tomate", "Atún", "Aceitunas",
		"Pollitos crunchy", "Bases de pizza", "Hielo",
		"Yogur natural", "Yogur edulcorado", "Batido +proteinas", "Leche proteica",
		"Pan de sándwich", "Palitos de frutos secos", "Bollitos de leche", 
		"Napolitana", "Pan", "Tila/Infusión", "Sopas",
		"Pipas aquasal", "Cacahuetes", "Cacahuetes desgrasado", "Pistachos", "Nueces",
		"Lasaña", "Tiras de pollo", "Tortilla de patatas", "Piña" 
	],
	"ALDI": ["Albóndigas de Soja", "Cereales 0%", "Queso Havarti", "Casera de Limón", "Gyozas de pollo"],
    "CARREFOUR": ["Patatas/Picoteo", "Monsters", "Mosto blanco"]
}

# =========================
# LOAD STATE
# =========================

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        checklist = data.get("checklist", default_checklist)
        state = data.get(
            "state",
            {item: False for sec in checklist.values() for item in sec}
        )
else:
    checklist = default_checklist
    state = {item: False for sec in checklist.values() for item in sec}

def save_state():
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"checklist": checklist, "state": state},
            f,
            ensure_ascii=False
        )

# =========================
# RENDER LIST
# =========================

def render_list():
    lines = []
    lines.append("🛒 LISTA DE LA COMPRA")
    lines.append("")

    for section, items in checklist.items():
        lines.append(section)
        for item in items:
            prefix = "✓" if state.get(item, False) else "   "
            lines.append(f"[{prefix}] {item}")
        lines.append("")

    return "```\n" + "\n".join(lines) + "\n```"

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(render_list(), parse_mode="Markdown")

async def toggle_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text.replace("/check", "").strip()

    if item not in state:
        await update.message.reply_text("Item no encontrado")
        return

    state[item] = not state[item]
    save_state()

    await update.message.reply_text(render_list(), parse_mode="Markdown")

async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/add", "").strip()

    if "|" not in text:
        await update.message.reply_text("Formato: /add SECCION | ITEM")
        return

    section, item = [x.strip() for x in text.split("|", 1)]

    if section not in checklist:
        checklist[section] = []

    checklist[section].append(item)
    state[item] = False
    save_state()

    await update.message.reply_text(render_list(), parse_mode="Markdown")

async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text.replace("/remove", "").strip()

    found = False
    for section, items in checklist.items():
        if item in items:
            items.remove(item)
            found = True
            break

    if not found:
        await update.message.reply_text("Item no encontrado")
        return

    state.pop(item, None)
    save_state()

    await update.message.reply_text(render_list(), parse_mode="Markdown")

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", start))
    app.add_handler(CommandHandler("check", toggle_item))
    app.add_handler(CommandHandler("add", add_item))
    app.add_handler(CommandHandler("remove", remove_item))

    print("Bot corriendo...")
    app.run_polling()
