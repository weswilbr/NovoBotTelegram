# NOME DO ARQUIVO: features/business/tables.py
# REFACTOR: Handler para o comando /tabelas, gerenciando o menu de tabelas de preços e pontos.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Estrutura de Dados Centralizada ---
# Centralizar as definições das tabelas torna a manutenção e adição de novas tabelas muito mais simples.
TABLE_ASSETS = {
    'precos': {'label': '📊 Tabela de Preços', 'type': 'submenu'},
    'pontos': {'label': '⭐ Tabela de Pontos', 'type': 'file', 'media_key': 'tabelapontos', 'file_type': 'photo'},
    'resgate': {'label': '💖 Tabela Resgate Fidelidade', 'type': 'file', 'media_key': 'tabelaresgate', 'file_type': 'photo'}
}

# --- Funções de Geração de Menu ---

def _get_main_menu() -> InlineKeyboardMarkup:
    """Gera o menu principal de tabelas dinamicamente."""
    keyboard = []
    for key, info in TABLE_ASSETS.items():
        # Define o callback_data com base no tipo de ação (abrir submenu ou enviar arquivo)
        callback_action = 'menu' if info['type'] == 'submenu' else 'send'
        keyboard.append([InlineKeyboardButton(info['label'], callback_data=f"tables_{callback_action}_{key}")])
    return InlineKeyboardMarkup(keyboard)

def _get_prices_submenu() -> InlineKeyboardMarkup:
    """Gera o submenu específico para tabelas de preços."""
    # Exemplo de como um submenu seria estruturado
    keyboard = [
        [
            InlineKeyboardButton("Atacado", callback_data="tables_send_precos_atacado"),
            InlineKeyboardButton("Varejo", callback_data="tables_send_precos_varejo")
        ],
        [InlineKeyboardButton("🔙 Voltar", callback_data="tables_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Handlers e Funções Auxiliares ---

async def tabelas_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /tabelas. Exibe ou edita para o menu principal de tabelas."""
    message_text = "📈 *Menu de Tabelas*\n\nSelecione a tabela que deseja consultar:"
    reply_markup = _get_main_menu()

    # Se a função foi chamada por um callback (ex: botão "Voltar"), edita a mensagem.
    if update.callback_query:
        await update.callback_query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode="Markdown")
    # Se foi chamada por um comando, envia uma nova mensagem.
    else:
        await update.message.reply_text(text=message_text, reply_markup=reply_markup, parse_mode="Markdown")

async def _show_prices_submenu(query: Update.callback_query) -> None:
    """Exibe o submenu de tabelas de preços."""
    message_text = "📊 *Tabelas de Preços*\n\nEscolha qual tabela de preços você quer ver:"
    reply_markup = _get_prices_submenu()
    await query.edit_message_text(text=message_text, reply_markup=reply_markup, parse_mode="Markdown")

async def _send_table_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, table_key: str) -> None:
    """Encontra e envia o arquivo de uma tabela específica."""
    # Busca a informação da tabela na nossa estrutura de dados
    asset_info = TABLE_ASSETS.get(table_key)
    
    # Busca a informação de qual tabela de preços foi pedida (ex: atacado, varejo)
    if table_key.startswith('precos_'):
        price_type = table_key.split('_')[-1] # 'atacado' ou 'varejo'
        asset_info = {'label': f'Tabela de Preços {price_type.capitalize()}', 'media_key': f'tabelapreco_{price_type}', 'file_type': 'photo'}

    if not asset_info:
        logger.warning(f"Chave de tabela desconhecida: {table_key}")
        return

    file_id = MEDIA.get('tabelas_gerais', {}).get(asset_info['media_key'])

    if not file_id:
        logger.warning(f"ID de arquivo não encontrado para tabela: '{asset_info['media_key']}'")
        await query.edit_message_text("⚠️ Desculpe, esta tabela não está disponível no momento.")
        return

    try:
        sender = context.bot.send_photo if asset_info['file_type'] == 'photo' else context.bot.send_document
        await sender(chat_id=query.message.chat.id, photo=file_id) # 'photo' funciona como 'document' para send_photo
        
        await query.edit_message_text(text=f"✅ A '{asset_info['label']}' foi enviada!", reply_markup=None)
    except TelegramError as e:
        logger.error(f"Erro ao enviar arquivo de tabela (ID: {file_id}): {e}")
        await query.edit_message_text("⚠️ Ocorreu um erro ao enviar a tabela. Tente novamente mais tarde.")

async def tables_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador para todos os callbacks que começam com 'tables_'."""
    query = update.callback_query
    await query.answer()

    if query.data == 'tables_main':
        await tabelas_menu(update, context)
        return

    try:
        # Ex: 'tables_send_pontos' -> ['tables', 'send', 'pontos']
        _, action_type, action_key = query.data.split('_', 2)
    except ValueError:
        logger.warning(f"Callback de tabelas mal formatado: {query.data}")
        return

    if action_type == 'send':
        await _send_table_file(query, context, action_key)
    elif action_type == 'menu' and action_key == 'precos':
        await _show_prices_submenu(query)

# NOTA PARA INTEGRAÇÃO EM main.py:
# Adicionar:
# from features.business import tables
#
# Em register_command_handlers:
# "tabelas": tables.tabelas_menu,
#
# Em register_callback_handlers:
# application.add_handler(CallbackQueryHandler(tables.tables_callback_handler, pattern='^tables_'))