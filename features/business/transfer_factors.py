# NOME DO ARQUIVO: features/business/transfer_factors.py
# REFACTOR: Handler para o comando /fatorestransferencia, com materiais educativos.
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

@group_member_required
async def fatorestransferencia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu sobre Fatores de Transferência."""
    keyboard = [
        [InlineKeyboardButton("🎥 Como funcionam", callback_data='fatorestransf_video1')],
        [InlineKeyboardButton("🎥 Animação", callback_data='fatorestransf_video2')],
        [InlineKeyboardButton("🎥 Os 3 R's", callback_data='fatorestransf_video3')],
        [InlineKeyboardButton("📄 Tabela de Porções", callback_data='fatorestransf_table')],
        [InlineKeyboardButton("▶️ Vídeo no YouTube", url="https://youtu.be/v-h387fXKcA")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📹 *Aprenda sobre os Fatores de Transferência:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def callback_fatorestransf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do menu de fatores de transferência."""
    query = update.callback_query
    key = query.data.split('_')[1]

    file_info = MEDIA.get('fatorestransf', {}).get(key)
    if not file_info:
        await context.bot.send_message(chat_id=query.message.chat.id, text="⚠️ Arquivo não encontrado.")
        return

    media_type, media_id = file_info['type'], file_info['id']
    sender = context.bot.send_video if media_type == 'video' else context.bot.send_document
    await sender(chat_id=query.message.chat.id, document=media_id)

