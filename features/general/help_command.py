# features/general/help_command.py
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ParseMode
from functools import wraps

# Placeholders para decorators
def group_member_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs): return await func(*args, **kwargs)
    return wrapper
def command_rate_limit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs): return await func(*args, **kwargs)
    return wrapper

@command_rate_limit
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    user_name = update.effective_user.first_name
    if update.message.chat.type == ChatType.PRIVATE:
        text = f"👋 Olá, *{user_name}*! Bem-vindo ao Assistente Virtual. Para ver todos os comandos, use /ajuda no nosso grupo principal."
    else:
        text = f"👋 Olá, *{user_name}*! Para ver a lista de comandos, digite /ajuda."
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

@group_member_required
@command_rate_limit
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de ajuda principal."""
    mensagem_ajuda = (
        "🌟 *Menu de Ajuda do Bot* 🌟\n\n"
        "Aqui estão os comandos que você pode usar:\n\n"
        "*/produtos* - Veja nosso catálogo de produtos.\n"
        "*/bonusconstrutor* - Entenda o Bônus Construtor.\n"
        "*/tabelas* - Acesse as tabelas de preços e pontos.\n"
        "*/eventos* - Confira os próximos eventos.\n"
        "*/fidelidade* - Saiba mais sobre o programa de fidelidade.\n"
        # Adicione outros comandos aqui
    )
    # A lógica de envio/edição da mensagem viria aqui
    if update.callback_query:
        await update.callback_query.edit_message_text(mensagem_ajuda, parse_mode='Markdown')
    else:
        await update.message.reply_text(mensagem_ajuda, parse_mode='Markdown')
