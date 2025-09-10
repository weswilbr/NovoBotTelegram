# NOME DO ARQUIVO: features/general/start.py
# REFACTOR: Contém a lógica do comando /start.
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ParseMode
from utils.anti_flood import command_rate_limit

@command_rate_limit
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a mensagem de boas-vindas ao usar o comando /start."""
    if not (update.message and update.effective_user and update.message.chat):
        return

    user_name = update.effective_user.first_name
    chat_type = update.message.chat.type

    if chat_type == ChatType.PRIVATE:
        mensagem = (
            f"👋 Olá, *{user_name}*\\! Bem\\-vindo\\(a\\) ao Assistente Virtual da *Equipe de Triunfo*\\! 🎉\n\n"
            "Para ter acesso completo a todas as funcionalidades, por favor, junte\\-se ao nosso grupo oficial e use os comandos por lá\\.\n\n"
            "💡 No grupo, digite /ajuda para ver a lista completa de comandos disponíveis\\."
        )
    else:
        mensagem = (
            f"👋 Olá, *{user_name}*\\! Você já está no grupo\\! 🎉\n\n"
            "Para ver a lista completa de comandos e funcionalidades, digite: /ajuda"
        )

    await update.message.reply_text(mensagem, parse_mode=ParseMode.MARKDOWN_V2)

