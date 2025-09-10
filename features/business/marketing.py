# NOME DO ARQUIVO: features/business/marketing.py
# REFACTOR: Handler para o comando /marketingrede, com opções de vídeo.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

@group_member_required
async def marketing_rede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe opções para o vídeo de Marketing de Rede."""
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

async def handle_download_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o vídeo de Marketing de Rede quando o botão de download é clicado."""
    query = update.callback_query
    video_id = MEDIA.get("marketing_rede", {}).get("video")
    if video_id:
        await context.bot.send_video(chat_id=query.message.chat.id, video=video_id)
    else:
        await query.message.reply_text("⚠️ Vídeo não encontrado.")

