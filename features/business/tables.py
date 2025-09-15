# NOME DO ARQUIVO: features/business/tables.py
# REFACTOR: Atualizado para usar a nova variável MEDIA_GERAL e com lógica de callback completa.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# CORREÇÃO: Importa MEDIA_GERAL em vez de MEDIA
from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

async def tabelas_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal de Tabelas."""
    if not (update.message or update.callback_query):
        return
        
    keyboard = [
        [InlineKeyboardButton("📊 Tabela de Preços", callback_data="tabela_precos")],
        [InlineKeyboardButton("⭐ Tabela de Pontos", callback_data="tabela_pontos")],
        [InlineKeyboardButton("💖 Tabela Resgate Fidelidade", callback_data="tabela_fidelidade")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "📈 *Menu de Tabelas*\n\nSelecione a tabela que deseja consultar:"
    
    # Se for um callback, edita a mensagem. Se for um comando, responde.
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=message_text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.message:
        await update.message.reply_text(
            text=message_text, reply_markup=reply_markup, parse_mode="Markdown"
        )

async def callback_tabelas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com todos os callbacks do menu de tabelas de forma segura."""
    query = update.callback_query
    if not (query and query.data and query.message):
        return

    await query.answer()
    
    # Extrai a ação do callback_data (ex: "precos", "pontos", "fidelidade")
    action_key = query.data.split('_')[1]
    chat_id = query.message.chat_id
    file_id = None

    try:
        # CORREÇÃO: Usa MEDIA_GERAL e acessa os dados de forma segura.
        # AVISO: Certifique-se de que a chave 'tabelas' e as subchaves
        # 'precos', 'pontos' e 'fidelidade' existam no seu general_media.yml
        file_id = MEDIA_GERAL.get('tabelas', {}).get(action_key)

        if file_id:
            # Assume-se que as tabelas são imagens (fotos), mas pode ser 'send_document'
            await context.bot.send_photo(chat_id=chat_id, photo=file_id, caption=f"Aqui está a Tabela de {action_key.capitalize()}.")
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Desculpe, a tabela de '{action_key}' não foi encontrada.")
            
    except Exception as e:
        logger.error(f"Erro ao processar callback de tabelas '{query.data}': {e}")
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Ocorreu um erro ao buscar a tabela.")