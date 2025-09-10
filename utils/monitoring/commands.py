# NOME DO ARQUIVO: utils/monitoring/commands.py
# REFACTOR: Comandos para administradores monitorarem o uso do bot.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_USER_IDS, CANAL_ID_2
from .tracker import UsageTracker

logger = logging.getLogger(__name__)

def admin_only(func):
    """Decorator para restringir o comando apenas a admins definidos na config."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not (update.effective_user and update.effective_user.id in ADMIN_USER_IDS):
            if update.message:
                await update.message.reply_text("Você não tem autorização para usar este comando.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

@admin_only
async def send_top_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a lista dos top 10 usuários para o chat de administração."""
    usage_tracker: UsageTracker | None = context.bot_data.get('usage_tracker')
    if not (usage_tracker and update.message):
        logger.error("UsageTracker não encontrado no context.bot_data.")
        if update.message: await update.message.reply_text("Erro: Módulo de monitoramento não inicializado.")
        return

    top_users = usage_tracker.get_top_users()
    if top_users:
        message = "*🏆 Top 10 Usuários de Comandos*\n\n"
        for i, (user_id, count) in enumerate(top_users):
            message += f"{i+1}. User ID: `{user_id}` - Comandos: {count}\n"
    else:
        message = "Nenhum dado de uso de comando disponível."

    # Envia para o admin que solicitou
    await update.message.reply_text(message, parse_mode='Markdown')

@admin_only
async def reset_usage_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reseta os dados de uso."""
    usage_tracker: UsageTracker | None = context.bot_data.get('usage_tracker')
    if not (usage_tracker and update.message):
        if update.message: await update.message.reply_text("Erro: Módulo de monitoramento não inicializado.")
        return
        
    usage_tracker.reset_data()
    await update.message.reply_text("Os dados de uso foram resetados.")

