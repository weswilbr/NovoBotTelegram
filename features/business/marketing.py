# NOME DO ARQUIVO: features/business/marketing.py
# Descreve o menu do vídeo de Marketing de Rede + callback para download.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# /marketingrede
# --------------------------------------------------------------------------- #
async def marketing_rede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu com opções para o vídeo de Marketing de Rede."""
    if not update.message:
        return

    keyboard = [
        [InlineKeyboardButton("🔗 Assista no YouTube",
                              url="https://www.youtube.com/watch?v=Fkeax_D_1m0")],
        [InlineKeyboardButton("⬇️ Baixar Vídeo",
                              callback_data="baixar_video_marketing")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Sem parse_mode para evitar erros de entity quando há emojis/asteriscos
    await update.message.reply_text(
        "📹 Vídeo de Marketing de Rede:\nEscolha uma das opções:",
        reply_markup=reply_markup,
    )

# --------------------------------------------------------------------------- #
# Callback para "Baixar Vídeo"
# --------------------------------------------------------------------------- #
async def callback_marketing_download(update: Update,
                                      context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o vídeo de Marketing de Rede quando o botão de download é clicado."""
    query = update.callback_query
    if not (query and query.message):
        return

    await query.answer()                       # remove o spinner
    chat_id = query.message.chat_id

    video_id = MEDIA_GERAL.get("marketing_rede", {}).get("video")

    try:
        if video_id:
            await context.bot.send_video(chat_id=chat_id, video=video_id)
        else:
            await context.bot.send_message(chat_id, "⚠️ Vídeo não encontrado.")
    except TelegramError as e:
        logger.error("Erro ao enviar vídeo de marketing: %s", e)
        await context.bot.send_message(chat_id, "⚠️ Ocorreu um erro ao tentar enviar o vídeo.")