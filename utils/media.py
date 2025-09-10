# NOME DO ARQUIVO: utils/media.py
# REFACTOR: Funções auxiliares para enviar diferentes tipos de mídia.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

async def send_media(update: Update, context: ContextTypes.DEFAULT_TYPE, media_key: str, sub_key: str, media_type: str):
    """Função genérica para enviar mídia."""
    chat_id = update.effective_chat.id if update.effective_chat else None
    if not chat_id: return

    file_id = MEDIA.get(media_key, {}).get(sub_key)
    if not file_id:
        logger.warning(f"Mídia não encontrada para {media_key}/{sub_key}")
        await context.bot.send_message(chat_id, "⚠️ Mídia não encontrada.")
        return

    try:
        if media_type == 'photo':
            await context.bot.send_photo(chat_id, photo=file_id)
        elif media_type == 'video':
            await context.bot.send_video(chat_id, video=file_id)
        elif media_type == 'document':
            await context.bot.send_document(chat_id, document=file_id)
    except Exception as e:
        logger.error(f"Erro ao enviar mídia {media_key}/{sub_key}: {e}")
        await context.bot.send_message(chat_id, "⚠️ Erro ao enviar a mídia.")

