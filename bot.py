# minecraft_telegram_bot/bot.py
import asyncio

from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, InlineQueryHandler, filters, ConversationHandler
)

from config import TOKEN, CONTAINER, logger, WORLD_NAME

from command_handlers import (
    start, help_command, login, logout, menu_command,
    logs_command, scarica_items_command, cmd_command,
    saveloc_command, edituser,
    give_direct_command, tp_direct_command, weather_direct_command,
    start_server_command, stop_server_command, restart_server_command,
    imnotcreative_command,
    backup_world_command,
    list_backups_command,
    add_resourcepack_command,
    edit_resourcepacks_command
)

from message_handlers import (
    handle_text_message, callback_query_handler, inline_query_handler,
    handle_document_message
)

async def set_bot_commands(application):
    commands = [
        BotCommand("menu", "🎒 Apri azioni rapide"),
        BotCommand("tp", "🚀 Teletrasportati"),
        BotCommand("weather", "☀️ Cambia meteo"),
        BotCommand("give", "🎁 Dai un oggetto"),
        BotCommand("saveloc", "📍 Salva posizione"),
        BotCommand("edituser", "👤 Modifica utente/posizioni"),
        BotCommand("cmd", "⚙️ Esegui comando server"),
        BotCommand("logs", "📄 Vedi log server"),
        BotCommand("backup_world", "💾 Backup mondo"),
        BotCommand("list_backups", "📂 Lista backup"),
        BotCommand("addresourcepack", "📦🖼️ Aggiungi resource pack"),
        BotCommand("editresourcepacks", "📦🛠️ Modifica resource pack"),
        BotCommand("scarica_items", "✨ Aggiorna lista item"),
        BotCommand("logout", "👋 Esci dal bot"),
        BotCommand("login", "🔑 Accedi al bot"),
        BotCommand("startserver", "▶️ Avvia server MC"),
        BotCommand("stopserver", "⏹️ Ferma server MC"),
        BotCommand("restartserver", "🔄 Riavvia server MC"),
        BotCommand("imnotcreative", "🛠️ Resetta flag creativo"),
        BotCommand("help", "❓ Aiuto comandi")
    ]
    try:
        await application.bot.set_my_commands(commands)
        logger.info("✅ Comandi Bot Telegram impostati.")
    except Exception as e:
        logger.error(f"❌ Errore impostazione comandi Bot: {e}", exc_info=True)

def main_sync():
    if not TOKEN:
        logger.critical("🚨 TOKEN Telegram mancante! Il bot non può avviarsi.")
        return
    if not CONTAINER: # Già loggato in config.py ma ribadire non fa male
        logger.warning("⚠️  CONTAINER non impostato in config. Funzionalità server limitate.")
    if not WORLD_NAME: # Già loggato in config.py
        logger.warning("⚠️  WORLD_NAME non impostato in config. Funzionalità mondo (backup, RP) limitate.")


    logger.info("🤖 Inizializzazione Bot Telegram...")
    application = ApplicationBuilder().token(TOKEN).build()

    loop = asyncio.get_event_loop()
    try:
        if loop.is_running():
            logger.info("⚙️ Loop asyncio attivo, creo task per set_bot_commands.")
            loop.create_task(set_bot_commands(application))
        else:
            logger.info("⚙️ Eseguo set_bot_commands in loop asyncio.")
            loop.run_until_complete(set_bot_commands(application))
    except RuntimeError as e:
        logger.error(f"⚙️❌ RuntimeError set_bot_commands in loop: {e}. Provare approccio diverso se in thread async.")
    except Exception as e:
        logger.error(f"🆘 Errore generico set_bot_commands: {e}", exc_info=True)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("logout", logout))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("logs", logs_command))
    application.add_handler(CommandHandler("scarica_items", scarica_items_command))
    application.add_handler(CommandHandler("cmd", cmd_command))
    application.add_handler(CommandHandler("saveloc", saveloc_command))
    application.add_handler(CommandHandler("edituser", edituser))
    application.add_handler(CommandHandler("give", give_direct_command))
    application.add_handler(CommandHandler("tp", tp_direct_command))
    application.add_handler(CommandHandler("weather", weather_direct_command))

    application.add_handler(CommandHandler("startserver", start_server_command))
    application.add_handler(CommandHandler("stopserver", stop_server_command))
    application.add_handler(CommandHandler("restartserver", restart_server_command))
    application.add_handler(CommandHandler("imnotcreative", imnotcreative_command))
    application.add_handler(CommandHandler("backup_world", backup_world_command))
    application.add_handler(CommandHandler("list_backups", list_backups_command))
    application.add_handler(CommandHandler("addresourcepack", add_resourcepack_command))
    application.add_handler(CommandHandler("editresourcepacks", edit_resourcepacks_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.Document.ALL & ~filters.COMMAND, handle_document_message))
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(InlineQueryHandler(inline_query_handler))

    logger.info("🤖 Bot avviato. In ascolto... 👂")
    application.run_polling()

if __name__ == "__main__":
    main_sync()