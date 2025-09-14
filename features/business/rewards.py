# NOME DO ARQUIVO: features/business/rewards.py
# REFACTOR: Handler para o comando /recompensas, enviando o plano de recompensas.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Constante do Módulo ---
# Centralizar o ID do documento aqui facilita a atualização no futuro.
# O nome 'recompensas2024' em MEDIA pode ser mantido, ou alterado para algo mais genérico.
REWARDS_DOCUMENT_ID = MEDIA.get('recompensas2024', {}).get('documento')

@group_member_required
async def mostrar_recompensas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /recompensas.
    Envia o documento do Plano de Recompensas para o usuário.
    """
    if not update.message:
        return

    # 1. Verifica se o ID do documento foi encontrado na configuração.
    if not REWARDS_DOCUMENT_ID:
        logger.warning("ID do documento de recompensas não foi encontrado em MEDIA.")
        await update.message.reply_text(
            "⚠️ Desculpe, o documento do Plano de Recompensas não está disponível no momento."
        )
        return

    # 2. Informa ao usuário que a solicitação está sendo processada (melhora a UX).
    await update.message.reply_text("Claro! Estou enviando o Plano de Recompensas atualizado...")

    # 3. Tenta enviar o documento e trata possíveis erros.
    try:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=REWARDS_DOCUMENT_ID,
            caption="Aqui está o Plano de Recompensas completo!"
        )
    except TelegramError as e:
        logger.error(f"Erro ao enviar o documento de recompensas (ID: {REWARDS_DOCUMENT_ID}): {e}")
        await update.message.reply_text(
            "⚠️ Ocorreu um erro ao tentar enviar o documento. A equipe de administração já foi notificada."
        )

# NOTA PARA INTEGRAÇÃO EM main.py:
# Lembre-se de atualizar a chamada no dicionário 'command_handlers':
#
# DE:
# "recompensas2024": rewards.recompensas2024,
#
# PARA:
# "recompensas": rewards.mostrar_recompensas,