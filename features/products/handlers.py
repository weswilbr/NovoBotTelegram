# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Gerencia o comando /produtos com menus de texto dinâmicos e visualmente aprimorados.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from telegram.constants import ParseMode

from utils.verification import group_member_required
from .data import MEDIA, PITCH_DE_VENDA_TEXT

logger = logging.getLogger(__name__)

# --- Funções de Geração de Texto para os Menus ---

def _get_main_menu_text() -> str:
    """Retorna o texto para o menu principal de produtos."""
    return (
        "🛍️ *Menu Principal de Produtos*\n\n"
        "Navegue por nossas categorias para encontrar materiais, vídeos e informações sobre cada produto.\n\n"
        "👇 *Selecione uma opção abaixo:*"
    )

def _get_individual_submenu_text() -> str:
    """Retorna o texto para o submenu de produtos individuais."""
    return (
        "📦 *Produtos Individuais*\n\n"
        "Explore nossa linha completa de produtos. Clique em um item para ver fotos, vídeos e materiais de venda."
    )

def _get_product_options_text(product_key: str) -> str:
    """Retorna o texto para o menu de opções de um produto específico."""
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    return f"Você selecionou: *{product_label}*\n\nO que você gostaria de ver sobre este produto?"


# --- Funções de Geração de Menu (Dinâmicas) ---

def _get_main_menu() -> InlineKeyboardMarkup:
    """Cria o menu principal de categorias de produtos."""
    keyboard = [
        [InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')],
    ]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
    """Gera dinamicamente o submenu com todos os produtos individuais."""
    buttons = []
    row = []
    for key, product_data in MEDIA.get('produtos', {}).items():
        label = product_data.get('label', key.capitalize())
        row.append(InlineKeyboardButton(label, callback_data=f'products_show_{key}'))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Voltar ao Menu Principal", callback_data='products_main')])
    return InlineKeyboardMarkup(buttons)

def _get_product_options_menu(product_key: str) -> InlineKeyboardMarkup:
    """Gera o menu de opções (foto, vídeo, pitch) para um produto específico."""
    product_data = MEDIA.get('produtos', {}).get(product_key, {})
    buttons = []
    if product_data.get('foto'):
        buttons.append(InlineKeyboardButton("📷 Ver Foto", callback_data=f"products_send_{product_key}_foto"))
    if product_data.get('video'):
        buttons.append(InlineKeyboardButton("🎥 Ver Vídeo", callback_data=f"products_send_{product_key}_video"))
    if product_data.get('documento'):
        buttons.append(InlineKeyboardButton("📄 Ver Documento", callback_data=f"products_send_{product_key}_documento"))
    if PITCH_DE_VENDA_TEXT.get(product_key):
        buttons.append(InlineKeyboardButton("📝 Pitch de Venda", callback_data=f"products_pitch_{product_key}"))
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Voltar para a Lista", callback_data='products_submenu_individual')])
    return InlineKeyboardMarkup(keyboard)


# --- Funções de Lógica e Handlers ---

@group_member_required
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /produtos. Exibe ou edita para o menu principal de produtos."""
    text = _get_main_menu_text()
    reply_markup = _get_main_menu()
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        elif update.message:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        logger.warning(f"Erro ao mostrar menu de produtos: {e}")

async def _show_individual_products_submenu(query: Update.callback_query) -> None:
    """Edita a mensagem para mostrar a lista de produtos individuais."""
    text = _get_individual_submenu_text()
    reply_markup = _get_individual_products_submenu()
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _show_product_options(query: Update.callback_query, product_key: str) -> None:
    """Edita a mensagem para mostrar as opções de um produto específico."""
    text = _get_product_options_text(product_key)
    reply_markup = _get_product_options_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_product_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, file_type: str) -> None:
    """Encontra e envia um arquivo (foto, vídeo, documento) de um produto."""
    file_id = MEDIA.get('produtos', {}).get(product_key, {}).get(file_type)
    if not file_id:
        await query.answer("⚠️ Mídia não encontrada.", show_alert=True)
        return
    try:
        sender_map = {'foto': context.bot.send_photo, 'video': context.bot.send_video, 'documento': context.bot.send_document}
        await sender_map[file_type](chat_id=query.message.chat.id, **{file_type: file_id})
        await query.edit_message_text(f"✅ Material enviado com sucesso!\n\nPara continuar, use o comando /produtos novamente.")
    except (TelegramError, KeyError) as e:
        logger.error(f"Erro ao enviar arquivo '{file_type}' do produto '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar a mídia.", show_alert=True)

async def _send_sales_pitch(query: Update.callback_query, product_key: str) -> None:
    """Envia a mensagem com o pitch de venda de um produto."""
    pitch_text = PITCH_DE_VENDA_TEXT.get(product_key)
    if not pitch_text:
        await query.answer("⚠️ Pitch de venda não encontrado.", show_alert=True)
        return
    try:
        await query.message.reply_text(pitch_text, parse_mode=ParseMode.MARKDOWN)
        await query.edit_message_text("✅ Pitch de venda enviado! Para continuar, use o comando /produtos novamente.")
    except TelegramError as e:
        logger.error(f"Erro ao enviar pitch de venda para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o texto.", show_alert=True)


async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador inteligente para todos os callbacks que começam com 'products_'."""
    query = update.callback_query
    await query.answer()
    try:
        data = query.data
        parts = data.split('_')
        action = parts[1]
        if action == 'main':
            await beneficiosprodutos(update, context)
        elif action == 'submenu':
            await _show_individual_products_submenu(query)
        elif action == 'show':
            await _show_product_options(query, parts[2])
        elif action == 'send':
            await _send_product_file(query, context, parts[2], parts[3])
        elif action == 'pitch':
            await _send_sales_pitch(query, parts[2])
    except (IndexError, TelegramError) as e:
        logger.error(f"Erro ao processar callback de produtos '{query.data}': {e}")
        try:
            await query.edit_message_text("Ocorreu um erro, te redirecionando para o menu principal.", reply_markup=_get_main_menu())
        except TelegramError:
            pass