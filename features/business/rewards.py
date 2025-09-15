# NOME DO ARQUIVO: features/business/rewards.py
# REFACTOR: Atualizado para usar a nova variável MEDIA_GERAL.

import logging
from telegram import Update
from telegram.ext import ContextTypes

# CORREÇÃO: Importa MEDIA_GERAL em vez de MEDIA
from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

async def recompensas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o documento do plano de recompensas para o usuário de forma segura."""
    if not update.message or not update.effective_chat:
        return

    # CORREÇÃO: Acessa MEDIA_GERAL de forma segura com o método .get()
    documento_id = MEDIA_GERAL.get('recompensas2024', {}).get('documento')
    
    if documento_id:
        try:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=documento_id,
                caption="📄 Aqui está o Plano de Recompensas atualizado."
            )
        except Exception as e:
            logger.error(f"Erro ao enviar o documento de recompensas: {e}")
            await update.message.reply_text("⚠️ Ocorreu um erro ao tentar enviar o documento.")
    else:
        await update.message.reply_text("⚠️ Documento de recompensas não encontrado.")