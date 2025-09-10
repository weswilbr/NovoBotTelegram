# NOME DO ARQUIVO: features/business/ranking.py
# REFACTOR: Gerencia a lógica para exibir o ranking de posições e seus detalhes.
import locale
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from telegram.ext import ContextTypes
from features.products.data import POSITIONS

def manual_format_currency(value):
    try:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return str(value)

def format_currency(value):
    if not isinstance(value, (int, float)):
        return format_value(value)
    try:
        return locale.currency(value, grouping=True, symbol='R$')
    except (locale.Error, TypeError, ValueError):
        return manual_format_currency(value)

def format_value(value, prefix="", suffix=""):
    if value is None: return "N/A"
    if isinstance(value, (int, float)):
        return f"{prefix}{value:n}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(value)

async def mostrar_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu com todas as posições do ranking."""
    keyboard = [
        [InlineKeyboardButton(f"{details.get('emoji', '▫️')} {name}", callback_data=f"detalhes_ranking_{name}")]
        for name, details in POSITIONS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💎 *Ranking de Posições*\n\nSelecione uma posição para ver os detalhes no seu privado.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def enviar_detalhes_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia os detalhes de uma posição específica no privado do usuário."""
    query = update.callback_query
    user_id = query.from_user.id
    bot_username = context.bot.username

    position_name = query.data.split("detalhes_ranking_")[1]
    position = POSITIONS.get(position_name)

    if not position:
        await query.answer("❌ Posição não encontrada.", show_alert=True)
        return

    linhas_qualificadas_str = "N/A"
    if position.get('linhas_qualificadas'):
        linhas_list = [f"{item['quantidade']} {item['posicao']}" for item in position['linhas_qualificadas']]
        linhas_qualificadas_str = ", ".join(linhas_list)

    message = "\n".join([
        f"{position.get('emoji', '▫️')} *{position_name}* - _{position.get('nivel_categoria', 'N/A')}_",
        "", "📋 *Requisitos:*",
        f"• PV Mensal: *{format_value(position.get('pv_mensal'), suffix=' PV')}*",
        f"• Linhas Qualificadas: *{linhas_qualificadas_str}*",
        f"• Volume Organizacional: *{format_value(position.get('vo_rede'), suffix=' VO')}*",
        "", "💰 *Ganhos e Benefícios:*",
        f"• Média de Ganhos: *{format_currency(position.get('media_ganho'))}*",
    ])
    try:
        await context.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")
        await query.answer("✅ Detalhes enviados no seu privado!")
    except error.Forbidden:
        await query.answer(f"Inicie uma conversa comigo: t.me/{bot_username}", show_alert=True)

