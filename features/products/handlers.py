# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Gerencia o comando /produtos e todos os submenus e callbacks relacionados.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from .data import MEDIA, PITCH_DE_VENDA_TEXT

logger = logging.getLogger(__name__)


def _get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')]]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
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

@group_member_required
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "🛍️ *Menu de Produtos*\n\nSelecione uma categoria:"
    reply_markup = _get_main_menu()
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        elif update.message:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except TelegramError as e:
        logger.warning(f"Erro ao mostrar menu de produtos: {e}")

async def _show_individual_products_submenu(query: Update.callback_query) -> None:
    text = "📦 *Produtos Individuais*\n\nSelecione um produto:"
    reply_markup = _get_individual_products_submenu()
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def _show_product_options(query: Update.callback_query, product_key: str) -> None:
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    text = f"Você selecionou: *{product_label}*\n\nEscolha o que deseja ver:"
    reply_markup = _get_product_options_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def _send_product_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, file_type: str) -> None:
    file_id = MEDIA.get('produtos', {}).get(product_key, {}).get(file_type)
    if not file_id:
        await query.answer("⚠️ Mídia não encontrada.", show_alert=True)
        return
    try:
        sender = getattr(context.bot, f"send_{file_type}")
        await sender(chat_id=query.message.chat.id, **{file_type: file_id})
        await query.edit_message_text(f"✅ Mídia enviada! Use /produtos para ver o menu novamente.")
    except (TelegramError, AttributeError) as e:
        logger.error(f"Erro ao enviar arquivo '{file_type}' do produto '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar a mídia.", show_alert=True)

async def _send_sales_pitch(query: Update.callback_query, product_key: str) -> None:
    pitch_text = PITCH_DE_VENDA_TEXT.get(product_key)
    if not pitch_text:
        await query.answer("⚠️ Pitch de venda não encontrado.", show_alert=True)
        return
    try:
        await query.message.reply_text(pitch_text, parse_mode='Markdown')
        await query.edit_message_text("✅ Pitch de venda enviado! Use /produtos para ver o menu novamente.")
    except TelegramError as e:
        logger.error(f"Erro ao enviar pitch de venda para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o texto.", show_alert=True)

async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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