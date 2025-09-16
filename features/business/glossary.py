# NOME DO ARQUIVO: features/business/glossary.py
# Handler /glossario + callbacks (menu, baixar PDF, voltar).

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from features.products.data import GLOSSARIO_TERMS, MEDIA_GERAL

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# /glossario – mostra o menu principal
# --------------------------------------------------------------------------- #
async def glossario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu do glossário."""
    keyboard: list[list[InlineKeyboardButton]] = []
    terms = sorted(GLOSSARIO_TERMS.keys())

    # dois botões por linha
    for i in range(0, len(terms), 2):
        row = [
            InlineKeyboardButton(terms[i].replace('_', ' ').title(),
                                 callback_data=f"glossario_{terms[i]}")
        ]
        if i + 1 < len(terms):
            row.append(
                InlineKeyboardButton(terms[i + 1].replace('_', ' ').title(),
                                     callback_data=f"glossario_{terms[i + 1]}")
            )
        keyboard.append(row)

    # botão para baixar PDF completo
    keyboard.append(
        [InlineKeyboardButton("📥 Baixar Glossário Completo",
                              callback_data="baixar_glossario")]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.answer()   # remove spinner
        await update.callback_query.edit_message_text(
            "Escolha um termo:", reply_markup=reply_markup
        )
    elif update.message:
        await update.message.reply_text(
            "Escolha um termo do glossário:", reply_markup=reply_markup
        )

# --------------------------------------------------------------------------- #
# Callback router para o glossário
# --------------------------------------------------------------------------- #
async def callback_glossario(update: Update,
                             context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks prefixados por 'glossario_' ou 'baixar_glossario'."""
    query = update.callback_query
    if not (query and query.data):
        return

    data = query.data
    await query.answer()                        # remove spinner imediatamente

    # 1) Download do PDF completo
    if data == "baixar_glossario":
        doc_id = MEDIA_GERAL.get("catalogoprodutos", {}).get("documento") \
                 or MEDIA_GERAL.get("glossario", {}).get("documento")
        if doc_id:
            try:
                await context.bot.send_document(query.message.chat_id, doc_id)
            except TelegramError as e:
                logger.error("Erro ao enviar PDF do glossário: %s", e)
                await query.message.reply_text("⚠️ Não foi possível enviar o documento.")
        else:
            await query.message.reply_text("⚠️ Documento não encontrado.")
        return

    # 2) Termo específico
    if data.startswith("glossario_"):
        term_key = data[len("glossario_"):]
        definition = GLOSSARIO_TERMS.get(term_key)
        if definition:
            back_button = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Voltar", callback_data="glossario_menu")]]
            )
            await query.edit_message_text(definition, reply_markup=back_button)
        else:
            await query.message.reply_text("⚠️ Termo não encontrado.")
        return

    # 3) Voltar ao menu principal
    if data == "glossario_menu":
        await glossario(update, context)

# --------------------------------------------------------------------------- #
# Export explícito
# --------------------------------------------------------------------------- #
__all__ = ["glossario", "callback_glossario"]