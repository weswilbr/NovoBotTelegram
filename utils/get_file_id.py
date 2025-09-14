# NOME DO ARQUIVO: utils/get_file_id.py
# FUNCIONALIDADE: Fornece um comando de desenvolvedor para obter o file_id de qualquer mídia.

import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters

logger = logging.getLogger(__name__)

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responde a uma mensagem com o file_id da mídia à qual o comando está respondendo.
    Este é um comando de utilidade para o administrador do bot.
    """
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ *Como usar:*\n"
            "1. Envie uma foto, vídeo, documento ou sticker.\n"
            "2. Responda a essa mídia com o comando `/getfileid`.",
            parse_mode='Markdown'
        )
        return

    replied_message = update.message.reply_to_message
    file_id = None
    media_type = "desconhecida"

    if replied_message.photo:
        # Pega a foto de maior resolução
        file_id = replied_message.photo[-1].file_id
        media_type = "Foto"
    elif replied_message.video:
        file_id = replied_message.video.file_id
        media_type = "Vídeo"
    elif replied_message.document:
        file_id = replied_message.document.file_id
        media_type = "Documento"
    elif replied_message.audio:
        file_id = replied_message.audio.file_id
        media_type = "Áudio"
    elif replied_message.sticker:
        file_id = replied_message.sticker.file_id
        media_type = "Sticker"
    elif replied_message.animation:
        file_id = replied_message.animation.file_id
        media_type = "Animação (GIF)"
        
    if file_id:
        logger.info(f"File ID para {media_type} obtido por {update.effective_user.id}: {file_id}")
        await update.message.reply_text(
            f"✅ *File ID da Mídia ({media_type}):*\n\n"
            f"`{file_id}`\n\n"
            "Copie este código e cole no seu arquivo `data.py`.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("⚠️ Nenhuma mídia encontrada na mensagem respondida.")

def get_file_id_handler() -> CommandHandler:
    """
    Cria e retorna o CommandHandler para o comando /getfileid.
    O filtro garante que este comando só funcione em conversas privadas com o bot,
    para não poluir os grupos.
    """
    return CommandHandler("getfileid", get_file_id, filters=filters.ChatType.PRIVATE)