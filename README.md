# Lista de la Compra Bot

Bot de Telegram en Python para gestionar una lista de la compra interactiva, organizada por supermercado, con checkboxes que se marcan directamente desde el chat.

## Características

- Lista de la compra organizada por secciones (por supermercado: Mercadona, Aldi, Carrefour), cada una con sus artículos.
- Teclado interactivo en Telegram (`InlineKeyboardMarkup`) donde cada artículo se marca/desmarca con un toque (✅/⬜).
- Comando `/start` para mostrar la lista completa con su teclado interactivo.
- Comando `/add Sección | Item` para añadir un nuevo artículo a una sección (creándola si no existe).
- Comando `/remove Item` para eliminar un artículo de la lista.
- Comando `/list` para ver la lista en formato texto plano, con el estado marcado/pendiente de cada artículo.
- Persistencia del estado y la lista en un fichero `state.json`, para que sobreviva a reinicios del bot.
- Preparado para desplegarse como worker en Railway (`Procfile`), leyendo el token del bot desde la variable de entorno `TOKEN`.

## Tecnologías

- Python
- `python-telegram-bot` (v20.3.0)
- JSON (persistencia simple en fichero)
- Railway (despliegue mediante `Procfile`, tipo `worker`)

## Instalación / Cómo ejecutarlo

1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Crea un bot en Telegram con [@BotFather](https://t.me/BotFather) y obtén su token.
3. Define el token como variable de entorno:
   ```
   export TOKEN="tu_token_de_telegram"
   ```
4. Ejecuta el bot:
   ```
   python checklist_bot.py
   ```
5. Abre una conversación con tu bot en Telegram y envía `/start` para ver la lista.

Para desplegarlo en Railway (o similar), basta con configurar la variable de entorno `TOKEN` en el servicio; el `Procfile` ya indica cómo arrancar el worker.

## Licencia

GPL versión 3 (ver archivo [LICENSE](LICENSE)).
