# NOME DO ARQUIVO: utils/error_handler.py
# REFACTOR: Handler global para capturar e logar exceções.
import logging
from telegram import Update
from telegram.ext import ContextTypes
import html
import traceback
import json

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loga os erros causados por updates e notifica o usuário."""
    logger.error("Exceção ao manusear um update:", exc_info=context.error)

    # Tenta notificar o usuário de que algo deu errado
    if isinstance(update, Update) and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Desculpe, ocorreu um erro inesperado. A equipe já foi notificada."
            )
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem de erro para o usuário: {e}")

