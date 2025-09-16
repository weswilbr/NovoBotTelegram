# NOME DO ARQUIVO: features/training/reading_guide.py
# REFACTOR: Handler para o comando /leitura, oferecendo o Guia do Êxito.
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

async def leitura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu para escolher a versão do Guia do Êxito."""
    keyboard = [
        [
            InlineKeyboardButton("📘 Versão em Português", callback_data='guia_exito_portugues'),
            InlineKeyboardButton("📕 Versão em Espanhol", callback_data='guia_exito_espanhol')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Escolha a versão do "Guia do êxito" para baixar:', reply_markup=reply_markup)

async def callback_leitura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o documento do Guia do Êxito no idioma selecionado."""
    query = update.callback_query
    
    file_id = None
    caption = None

    if query.data == 'guia_exito_portugues':
        file_id = MEDIA['reading_guide']['portugues']
        caption = "📘 Guia do êxito em Português!"
    elif query.data == 'guia_exito_espanhol':
        file_id = MEDIA['reading_guide']['espanhol']
        caption = "📕 Guia do êxito em Espanhol!"

    if file_id:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id, caption=caption)

