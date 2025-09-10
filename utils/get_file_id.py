# NOME DO ARQUIVO: utils/get_file_id.py
# REFACTOR: Handler para administradores obterem o file_id de mídias.
import logging
from telegram import Update, ChatMember
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from config import ADMIN_USER_IDS

logger = logging.getLogger(__name__)

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Captura e retorna o file_id de mídias enviadas por admins."""
    if not (update.message and update.effective_user and update.effective_chat): return
    
    user = update.effective_user
    chat = update.effective_chat
    
    # Autorização: admin global ou criador do grupo
    is_authorized = user.id in ADMIN_USER_IDS
    if not is_authorized and chat.type != 'private':
        try:
            member = await context.bot.get_chat_member(chat.id, user.id)
            if member.status == ChatMember.OWNER:
                is_authorized = True
        except Exception as e:
            logger.error(f"Não foi possível verificar se {user.id} é criador do chat {chat.id}: {e}")

    if not is_authorized: return

    media_map = {
        'photo': ('🖼️ Foto', update.message.photo[-1]),
        'video': ('🎥 Vídeo', update.message.video),
        'document': ('📄 Documento', update.message.document),
        'audio': ('🎵 Áudio', update.message.audio),
        'animation': ('🎞️ Animação', update.message.animation),
        'sticker': ('🌟 Sticker', update.message.sticker),
    }

    for key, (emoji, media_obj) in media_map.items():
        if hasattr(update.message, key) and media_obj:
            file_id = media_obj.file_id
            unique_id = media_obj.file_unique_id
            text = (f"{emoji} ID: `{escape_markdown(file_id, version=2)}`\n"
                    f"🔒 ID Único: `{escape_markdown(unique_id, version=2)}`")
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)
            break

def get_file_id_handler() -> MessageHandler:
    """Retorna um MessageHandler configurado para capturar file IDs."""
    media_filters = (filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.Document.ALL | filters.ANIMATION | filters.Sticker.ALL)
    return MessageHandler(media_filters, get_file_id)

