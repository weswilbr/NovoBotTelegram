# NOME DO ARQUIVO: features/community/private_messaging.py
# REFACTOR: Gerencia mensagens recebidas em chats privados com o bot.
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lida com mensagens de texto em chats privados, com verificações de segurança."""

    # Adiciona verificações para garantir que os objetos necessários não são None
    if not update.message or not update.effective_user:
        logger.warning("handle_private_message chamado com um update sem 'message' ou 'effective_user'.")
        return

    user_id = update.effective_user.id
    message_text = update.message.text

    # A verificação de context.user_data é segura, pois ele é inicializado pela biblioteca.
    if context.user_data and ('id_afiliado' in context.user_data or context.user_data.get("__conversation__state") is not None):
        logger.info(f"Ignorando mensagem de {user_id} porque está em uma conversa.")
        return

    # Lida com casos de mensagens sem texto (ex: foto, sticker em chat privado)
    if not message_text:
        logger.info(f"Usuário {user_id} enviou uma mensagem sem texto no privado.")
        await update.message.reply_text(
            "Olá! Para ver o que posso fazer, por favor, interaja usando os comandos no nosso grupo."
        )
        return

    # Comandos são tratados por CommandHandlers, então este handler deve ignorá-los.
    if message_text.startswith('/'):
        logger.info(f"Usuário {user_id} enviou um comando no privado, que será tratado por outro handler.")
        return
    else:
        logger.info(f"Usuário {user_id} enviou texto no privado, mas não é um comando.")
        await update.message.reply_text(
            "Olá! Sou um bot de assistência. Para ver a lista completa de comandos e funcionalidades, por favor, use o comando /ajuda em nosso grupo de suporte."
        )

