# NOME DO ARQUIVO: features/business/rewards.py
# REFACTOR: Handler para o comando /recompensas2024, enviando o plano de recompensas.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

@group_member_required
async def recompensas2024(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o documento de recompensas 2024 para o usuário."""
    documento_id = MEDIA['recompensas2024'].get('documento')
    if documento_id:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=documento_id)
    else:
        await update.message.reply_text("⚠️ Documento de recompensas não encontrado.")

