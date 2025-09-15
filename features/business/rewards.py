# NOME DO ARQUIVO: features/business/rewards.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

@group_member_required
# CORREÇÃO: A função foi renomeada para 'recompensas'
async def recompensas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o documento do plano de recompensas para o usuário."""
    documento_id = MEDIA['recompensas2024'].get('documento')
    if documento_id:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=documento_id)
    else:
        await update.message.reply_text("⚠️ Documento de recompensas não encontrado.")