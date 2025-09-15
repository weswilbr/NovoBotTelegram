# NOME DO ARQUIVO: features/business/factory.py
# REFACTOR: Handler para o comando /fabrica4life, exibindo vídeos da fábrica.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

async def fabrica4life(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de vídeos da Fábrica 4Life."""
    keyboard = [
        [InlineKeyboardButton("🏬 Armazém 4Life", callback_data='fabrica_armazem')],
        [InlineKeyboardButton("🏭 Envase de Produtos", callback_data='fabrica_envase')],
        [InlineKeyboardButton("🏗️ Nova Fábrica 4Life", callback_data='fabrica_novafabrica')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🏭 *Escolha um vídeo para visualizar:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def callback_fabrica4life(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do menu da fábrica."""
    query = update.callback_query
    action = query.data.split('_')[1]

    video_ids = MEDIA['fabrica4life'].get(action)
    if not video_ids:
        await query.edit_message_text("⚠️ Vídeo não encontrado.")
        return

    if not isinstance(video_ids, list):
        video_ids = [video_ids]

    for video_id in video_ids:
        await context.bot.send_video(chat_id=query.message.chat.id, video=video_id)