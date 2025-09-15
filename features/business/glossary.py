# NOME DO ARQUIVO: features/business/glossary.py
# REFACTOR: Handler para o comando /glossario, exibindo termos e suas definições.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import GLOSSARIO_TERMS, MEDIA

logger = logging.getLogger(__name__)

async def glossario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu do glossário."""
    keyboard = []
    terms = list(GLOSSARIO_TERMS.keys())
    for i in range(0, len(terms), 2):
        row = [InlineKeyboardButton(terms[i].replace('_', ' ').title(), callback_data=f"glossario_{terms[i]}")]
        if i + 1 < len(terms):
            row.append(InlineKeyboardButton(terms[i+1].replace('_', ' ').title(), callback_data=f"glossario_{terms[i+1]}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("📥 Baixar Glossário Completo", callback_data='baixar_glossario')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text("Escolha um termo:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Escolha um termo do glossário:", reply_markup=reply_markup)


async def callback_glossario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do glossário."""
    query = update.callback_query
    action = query.data.split('_')[-1]

    if action == 'glossario': # Voltar ao menu
        await glossario(update, context)
        return

    if action == 'baixar':
        doc_id = MEDIA['glossario'].get('documento')
        await context.bot.send_document(chat_id=query.message.chat.id, document=doc_id)
    elif action in GLOSSARIO_TERMS:
        definition = GLOSSARIO_TERMS[action]
        await query.edit_message_text(f"{definition}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data='glossario_glossario')]]))