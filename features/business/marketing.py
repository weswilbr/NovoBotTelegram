# NOME DO ARQUIVO: features/business/marketing.py
# REFACTOR: Atualizado para usar a nova variável MEDIA_GERAL.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

# CORREÇÃO: Importa MEDIA_GERAL em vez de MEDIA
from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

async def marketing_rede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe opções para o vídeo de Marketing de Rede."""
    if not update.message:
        return

    keyboard = [
        [InlineKeyboardButton("🔗 Assista no YouTube", url="https://www.youtube.com/watch?v=Fkeax_D_1m0")],
        [InlineKeyboardButton("⬇️ Baixar Vídeo", callback_data="baixar_video_marketing")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📹 *Vídeo de Marketing de Rede:*\nEscolha uma das opções:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def callback_marketing_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o vídeo de Marketing de Rede quando o botão de download é clicado."""
    query = update.callback_query
    if not (query and query.message):
        return

    await query.answer()
    chat_id = query.message.chat_id

    # CORREÇÃO: Usa MEDIA_GERAL e .get() para segurança
    video_id = MEDIA_GERAL.get("marketing_rede", {}).get("video")
    
    try:
        if video_id:
            await context.bot.send_video(chat_id=chat_id, video=video_id)
        else:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Vídeo não encontrado.")
    except TelegramError as e:
        logger.error(f"Erro em callback_marketing_download ao enviar mídia: {e}")
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Ocorreu um erro ao tentar enviar o vídeo.")