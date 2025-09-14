# NOME DO ARQUIVO: utils/monitoring/commands.py
# REFACTOR: Simplificado para ler nomes diretamente dos dados salvos pelo tracker.

from telegram import Update
from telegram.ext import ContextTypes
from .tracker import UsageTracker

async def send_top_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem com o ranking dos usuários mais ativos."""
    tracker: UsageTracker = context.bot_data.get("usage_tracker")
    if not tracker:
        await update.message.reply_text("Erro: O módulo de rastreamento não foi inicializado.")
        return

    top_users = tracker.get_top_users(top_n=10)

    if not top_users:
        await update.message.reply_text("Ainda não há dados de uso para exibir.")
        return

    # Monta a mensagem usando os dados salvos (nome e contagem)
    message_lines = ["🏆 *Ranking de Usuários Mais Ativos* 🏆\n"]
    # O formato de top_users agora é [('user_id', {'name': 'Nome', 'count': X}), ...]
    for i, (user_id, data) in enumerate(top_users):
        user_name = data.get('name', f"ID {user_id}") # Pega o nome, com um fallback para o ID
        count = data.get('count', 0)
        message_lines.append(f"{i + 1}. {user_name} - {count} comandos")

    response_message = "\n".join(message_lines)
    await update.message.reply_text(response_message, parse_mode='Markdown')

async def reset_usage_data_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reseta todos os dados de uso."""
    tracker: UsageTracker = context.bot_data.get("usage_tracker")
    if not tracker:
        await update.message.reply_text("Erro: O módulo de rastreamento não foi inicializado.")
        return
        
    tracker.reset_data()
    await update.message.reply_text("✅ Todos os dados de uso foram resetados com sucesso!")