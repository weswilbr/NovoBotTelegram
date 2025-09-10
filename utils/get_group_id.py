# NOME DO ARQUIVO: utils/get_group_id.py
# REFACTOR: Handler para obter o ID do grupo atual.
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia o ID do grupo em uma mensagem privada para o usuário."""
    if not (update.effective_chat and update.effective_user and update.effective_message):
        return

    if update.effective_chat.type in ["group", "supergroup"]:
        group_id = update.effective_chat.id
        user_id = update.effective_user.id
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"O ID deste grupo é: `{group_id}`",
                parse_mode="MarkdownV2"
            )
            await update.effective_message.reply_text("O ID do grupo foi enviado para o seu privado.")
        except Exception:
            await update.effective_message.reply_text("Não consegui enviar o ID para o seu privado. Inicie uma conversa comigo primeiro.")
    else:
        await update.effective_message.reply_text("Este comando só funciona em grupos.")

def setup_group_id_handler() -> CommandHandler:
    """Retorna um CommandHandler para o comando /get_group_id."""
    return CommandHandler("getgroupid", get_group_id)

