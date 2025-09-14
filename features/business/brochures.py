# NOME DO ARQUIVO: features/business/brochures.py
# REFACTOR: Handler para o comando /folheteria, exibindo catálogos e panfletos.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

# Assumindo que este decorator verifica se o usuário está no grupo principal.
from utils.verification import group_member_required 
# Centralize a importação de dados de mídia.
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Mapeamento de Documentos ---
# Centralizar a busca dos IDs em um dicionário torna o código mais limpo
# e fácil de adicionar novos documentos no futuro.
BROCHURE_DOCUMENTS = {
    'panfletos': MEDIA.get('folheteria', {}).get('panfletoprodutosnovo'),
    'catalogo': MEDIA.get('catalogoprodutos', {}).get('documento'),
    'enquete': MEDIA.get('enqueteimunidade', {}).get('id')
}

def get_brochures_menu() -> InlineKeyboardMarkup:
    """Cria e retorna o menu principal de folheteria."""
    # Usar um prefixo consistente (ex: 'brochure_') facilita o roteamento dos callbacks.
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📰 Ver Panfletos", callback_data='brochure_panfletos')],
        [InlineKeyboardButton("📔 Catálogo 4Life", callback_data='brochure_catalogo')],
        [InlineKeyboardButton("📊 Enquete Imunidade", callback_data='brochure_enquete')],
    ])

@group_member_required
async def folheteria(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /folheteria.
    Exibe um menu com opções de materiais para o usuário.
    """
    await update.message.reply_text(
        "👋 Bem-vindo à seção de materiais!\n\n"
        "Escolha uma das opções abaixo para receber o documento:",
        reply_markup=get_brochures_menu()
    )

async def brochures_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lida com os callbacks dos botões do menu de folheteria.
    Este handler deve ser registrado em main.py com o pattern='^brochure_'.
    """
    query = update.callback_query
    # É uma boa prática sempre responder ao callback para remover o ícone de "carregando".
    await query.answer()

    # Extrai a ação do callback_data. Ex: 'brochure_panfletos' -> 'panfletos'
    action = query.data.split('_', 1)[1]

    doc_id = BROCHURE_DOCUMENTS.get(action)

    if not doc_id:
        logger.warning(f"ID de documento não encontrado para a ação de folheteria: '{action}'")
        await query.edit_message_text(
            "⚠️ Desculpe, este material não está disponível no momento. Tente novamente mais tarde."
        )
        return

    try:
        # Envia o documento para o usuário.
        await context.bot.send_document(
            chat_id=query.message.chat.id,
            document=doc_id,
            caption=f"Aqui está o material sobre '{action.capitalize()}' que você solicitou!"
        )
        
        # Edita a mensagem original para remover os botões e confirmar o envio.
        # Isso previne que o usuário clique nos botões novamente.
        await query.edit_message_text(
            text="✅ Documento enviado com sucesso! Verifique acima.",
            reply_markup=None # Remove o teclado inline
        )

    except TelegramError as e:
        logger.error(f"Erro ao enviar documento de folheteria (ID: {doc_id}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao tentar enviar o documento. A equipe de administração já foi notificada."
        )

# NOTA PARA INTEGRAÇÃO EM main.py:
# O handler 'brochures_callback_handler' deve ser registrado junto aos outros CallbackQueryHandlers.
# Exemplo de como adicioná-lo:
# from features.business.brochures import brochures_callback_handler
# application.add_handler(CallbackQueryHandler(brochures_callback_handler, pattern='^brochure_'))