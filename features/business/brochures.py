# NOME DO ARQUIVO: features/business/brochures.py
# REFACTOR: Handler para o comando /folheteria, atualizado para usar MEDIA_GERAL.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# CORREÇÃO: Importa MEDIA_GERAL em vez de MEDIA
from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

def get_main_menu() -> InlineKeyboardMarkup:
    """Cria o menu de botões para a seção de folheteria."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📰 Ver Panfletos", callback_data='folheteria_panfletos')],
        [InlineKeyboardButton("📔 Catálogo 4Life", callback_data='folheteria_catalogo')],
        # [InlineKeyboardButton("📊 Enquete Imunidade", callback_data='folheteria_enquete')], # Descomente se você adicionar 'enqueteimunidade' ao seu YML
    ])

async def folheteria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal de Folheteria."""
    if not update.message:
        return
    await update.message.reply_text(
        "👋 Escolha uma opção para ver os materiais:",
        reply_markup=get_main_menu()
    )

async def callback_folheteria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks de folheteria de forma segura."""
    query = update.callback_query
    if not (query and query.data and query.message):
        return
    
    await query.answer()
    
    action = query.data.split('_')[1]
    chat_id = query.message.chat_id
    doc_id = None

    try:
        # CORREÇÃO: Usa MEDIA_GERAL e o método .get() para segurança
        if action == 'panfletos':
            doc_id = MEDIA_GERAL.get('folheteria', {}).get('panfletoprodutosnovo')
        elif action == 'catalogo':
            doc_id = MEDIA_GERAL.get('catalogoprodutos', {}).get('documento')
        elif action == 'enquete':
            # AVISO: A chave 'enqueteimunidade' não foi encontrada nos seus dados.
            # Este código evita que o bot quebre, mas o documento não será encontrado.
            doc_id = MEDIA_GERAL.get('enqueteimunidade', {}).get('id')

        # Lógica centralizada para enviar o documento ou avisar o usuário
        if doc_id:
            await context.bot.send_document(chat_id=chat_id, document=doc_id)
        else:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Desculpe, este material não foi encontrado.")
            
    except Exception as e:
        logger.error(f"Erro ao processar callback de folheteria '{query.data}': {e}")
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Ocorreu um erro ao buscar o material.")