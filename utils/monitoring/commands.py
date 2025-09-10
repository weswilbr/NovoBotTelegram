# NOME DO ARQUIVO: utils/monitoring/commands.py
# REFACTOR: Contém os handlers de comando para as funcionalidades de monitoramento.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import CANAL_ID_2, ADMIN_USER_IDS
from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# --- Handlers de Comando ---

@group_member_required
async def send_top_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a lista dos top 10 usuários para o canal de administradores."""
    if 'usage_tracker' not in context.bot_data:
        logger.error("Usage tracker não encontrado em context.bot_data!")
        if update.message:
            await update.message.reply_text("Erro: O rastreador de uso não foi inicializado.")
        return

    usage_tracker = context.bot_data['usage_tracker']
    top_users = usage_tracker.get_top_users()

    if top_users:
        message = "*🏆 Top 10 Usuários de Comandos (Semanal) 🏆*\n\n"
        for i, (user_id, count) in enumerate(top_users):
            message += f"{i+1}. User ID: `{user_id}` - Comandos: {count}\n"
        message += "\nContinue usando os comandos!"
    else:
        message = "Nenhum dado de uso de comando disponível ainda."

    try:
        if CANAL_ID_2 and update.message:
             await context.bot.send_message(chat_id=CANAL_ID_2, text=message, parse_mode='Markdown')
             await update.message.reply_text("Relatório enviado para o canal de administração.")
             logger.info("Lista de top usuários enviada com sucesso.")
        else:
            logger.warning("CANAL_ID_2 não definido. Não foi possível enviar a lista de top usuários.")
            if update.message:
                await update.message.reply_text("O canal de destino não está configurado.")
    except Exception as e:
        logger.error(f"Erro ao enviar a lista de top usuários: {e}")
        if update.message:
            await update.message.reply_text("Ocorreu um erro ao enviar a lista.")

async def reset_usage_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reseta os dados de uso. Requer privilégios de administrador."""
    user = update.effective_user
    if not user or user.id not in ADMIN_USER_IDS:
        if update.message:
            await update.message.reply_text("Você não tem autorização para executar esta ação.")
        return

    if 'usage_tracker' not in context.bot_data:
        logger.error("Usage tracker não encontrado em context.bot_data para reset!")
        if update.message:
            await update.message.reply_text("Erro: O rastreador de uso não foi inicializado.")
        return

    usage_tracker = context.bot_data['usage_tracker']
    usage_tracker.reset_data()
    logger.warning(f"Os dados de uso foram resetados pelo administrador {user.id}.")
    if update.message:
        await update.message.reply_text("Os dados de uso foram resetados com sucesso.")

