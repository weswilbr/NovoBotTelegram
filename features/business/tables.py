# NOME DO ARQUIVO: features/business/tables.py
# Menu de Tabelas (preço, pontos, fidelidade) – sem erro de Markdown.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# /tabelas  →  menu principal
# --------------------------------------------------------------------------- #
async def tabelas_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal de Tabelas."""
    if not (update.message or update.callback_query):
        return

    keyboard = [
        [InlineKeyboardButton("📊 Tabela de Preços", callback_data="tabela_preco")],
        [InlineKeyboardButton("⭐ Tabela de Pontos",  callback_data="tabela_pontos")],
        [InlineKeyboardButton("💖 Tabela Resgate Fidelidade", callback_data="tabela_fidelidade")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "📈 Menu de Tabelas\n\nSelecione a tabela que deseja consultar:"

    # envia ou edita mensagem SEM parse_mode para evitar BadRequest
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

# --------------------------------------------------------------------------- #
# Callback router
# --------------------------------------------------------------------------- #
async def callback_tabelas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do menu de tabelas."""
    query = update.callback_query
    if not (query and query.data and query.message):
        return

    await query.answer()                         # remove spinner
    chat_id = query.message.chat_id

    # data = "tabela_preco" / "tabela_pontos" / "tabela_fidelidade"
    action_key = query.data.split('_')[1]        # preco / pontos / fidelidade

    # mapeia para a chave no YAML (precos ≠ preco)
    yaml_key = "precos" if action_key == "preco" else action_key
    file_id = MEDIA_GERAL.get("tabelas", {}).get(yaml_key)

    if not file_id:
        await context.bot.send_message(
            chat_id, f"⚠️ Desculpe, a tabela de '{action_key}' não foi encontrada."
        )
        return

    try:
        # Assume imagem; troque para send_document se for PDF
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=file_id,
            caption=f"Aqui está a tabela de {action_key.capitalize()}."
        )
    except TelegramError as e:
        logger.error("Erro ao enviar tabela %s: %s", action_key, e)
        await context.bot.send_message(chat_id, "⚠️ Ocorreu um erro ao enviar a tabela.")

# --------------------------------------------------------------------------- #
__all__ = ["tabelas_menu", "callback_tabelas"]