# NOME DO ARQUIVO: features/business/brochures.py
# REFACTOR: Handler para o comando /folheteria, exibindo catálogos e panfletos.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📰 Ver Panfletos", callback_data='folheteria_panfletos')],
        [InlineKeyboardButton("📔 Catálogo 4Life", callback_data='folheteria_catalogo')],
        [InlineKeyboardButton("📊 Enquete Imunidade", callback_data='folheteria_enquete')],
    ])

async def folheteria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal de Folheteria."""
    await update.message.reply_text(
        "👋 Escolha uma opção para ver os materiais:",
        reply_markup=get_main_menu()
    )

async def callback_folheteria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks de folheteria."""
    query = update.callback_query
    action = query.data.split('_')[1]

    if action == 'panfletos':
        # Adicionar submenu se houver mais de um panfleto
        doc_id = MEDIA['folheteria'].get('panfletoprodutosnovo')
        await context.bot.send_document(chat_id=query.message.chat.id, document=doc_id)
    elif action == 'catalogo':
        doc_id = MEDIA['catalogoprodutos'].get('documento')
        await context.bot.send_document(chat_id=query.message.chat.id, document=doc_id)
    elif action == 'enquete':
        doc_id = MEDIA['enqueteimunidade'].get('id')
        await context.bot.send_document(chat_id=query.message.chat.id, document=doc_id)