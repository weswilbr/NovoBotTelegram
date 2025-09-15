# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Gerencia o comando /produtos com um "Kit de Mídia Social" padronizado e completo.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from telegram.constants import ParseMode

from .data import MEDIA, PITCH_DE_VENDA_TEXT

logger = logging.getLogger(__name__)

# --- Funções de Geração de Texto ---
def _get_main_menu_text() -> str:
    return "🛍️ *Menu Principal de Produtos*\n\nNavegue por nossas categorias para encontrar materiais e ferramentas de marketing para cada produto."

def _get_individual_submenu_text() -> str:
    return "📦 *Produtos Individuais*\n\nSelecione um produto para ver os detalhes e acessar seu kit de marketing."

def _get_product_options_text(product_key: str) -> str:
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    return f"Você selecionou: *{product_label}*\n\nO que você gostaria de ver ou usar?"

# --- Funções de Geração de Menu (Inline Keyboards) ---
def _get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')]]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
    buttons, row = [], []
    product_items = MEDIA.get('produtos', {})
    if isinstance(product_items, dict):
        for key, data in product_items.items():
            if isinstance(data, dict):
                label = data.get('label', key.capitalize())
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
    if product_data.get('social_kit'):
        buttons.append(InlineKeyboardButton("📲 Kit de Mídia Social", callback_data=f"products_social_{product_key}"))
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Voltar para a Lista", callback_data='products_submenu_individual')])
    return InlineKeyboardMarkup(keyboard)

def _get_social_kit_menu(product_key: str) -> InlineKeyboardMarkup:
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    buttons = []
    if kit_data.get('copy_text'):
        buttons.append(InlineKeyboardButton("📝 Texto p/ Post", callback_data=f"products_social_send_text_{product_key}"))
    if kit_data.get('story_image'):
        buttons.append(InlineKeyboardButton("🖼️ Imagem p/ Stories", callback_data=f"products_social_send_story_{product_key}"))
    if kit_data.get('feed_image'):
        buttons.append(InlineKeyboardButton("🏞️ Imagem p/ Feed", callback_data=f"products_social_send_feed_{product_key}"))
    if kit_data.get('reels_video'):
        buttons.append(InlineKeyboardButton("🎬 Vídeo p/ Reels", callback_data=f"products_social_send_reels_{product_key}"))
    if kit_data.get('hashtags'):
        buttons.append(InlineKeyboardButton("#️⃣ Hashtags", callback_data=f"products_social_send_tags_{product_key}"))
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton(f"🔙 Voltar para o Produto", callback_data=f"products_show_{product_key}")])
    return InlineKeyboardMarkup(keyboard)

# --- Handlers de Lógica ---
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    text = _get_main_menu_text()
    reply_markup = _get_main_menu()
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _show_main_menu(query, **kwargs) -> None:
    text = _get_main_menu_text()
    reply_markup = _get_main_menu()
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        if "message is not modified" not in str(e).lower():
            logger.warning(f"Erro ao editar para o menu principal: {e}")

async def _show_individual_products_submenu(query, parts=None, **kwargs) -> None:
    text = _get_individual_submenu_text()
    reply_markup = _get_individual_products_submenu()
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _show_product_options(query, parts: list, **kwargs) -> None:
    product_key = parts[2]
    text = _get_product_options_text(product_key)
    reply_markup = _get_product_options_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_media_and_cleanup(query, context: ContextTypes.DEFAULT_TYPE, sender_callable, file_id: str, media_type: str) -> None:
    try:
        await sender_callable(chat_id=query.message.chat.id, **{media_type: file_id})
        await query.edit_message_text(f"✅ Material enviado!\n\nUse /produtos para voltar ao menu.", reply_markup=None)
    except (TelegramError, KeyError) as e:
        logger.error(f"Erro ao enviar {media_type} com ID {file_id}: {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar a mídia.", show_alert=True)

async def _send_product_file(query, context: ContextTypes.DEFAULT_TYPE, parts: list, **kwargs) -> None:
    product_key, file_type = parts[2], parts[3]
    file_id = MEDIA.get('produtos', {}).get(product_key, {}).get(file_type)
    if not file_id:
        await query.answer("⚠️ Mídia não encontrada.", show_alert=True)
        return
    sender_map = {'foto': context.bot.send_photo, 'video': context.bot.send_video, 'documento': context.bot.send_document}
    await _send_media_and_cleanup(query, context, sender_map[file_type], file_id, file_type)

async def _send_sales_pitch(query, context: ContextTypes.DEFAULT_TYPE, parts: list, **kwargs) -> None:
    product_key = parts[2]
    pitch_text = PITCH_DE_VENDA_TEXT.get(product_key)
    if not pitch_text:
        await query.answer("⚠️ Pitch de venda não encontrado.", show_alert=True)
        return
    await query.message.reply_text(pitch_text, parse_mode=ParseMode.MARKDOWN)
    await query.answer("✅ Pitch enviado!")

async def _show_social_kit_menu(query, parts: list, **kwargs) -> None:
    product_key = parts[2]
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    text = f"📲 *Kit de Mídia Social: {product_label}*\n\nUse estas ferramentas para impulsionar suas vendas!"
    reply_markup = _get_social_kit_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_social_kit_asset(query, context: ContextTypes.DEFAULT_TYPE, parts: list, **kwargs):
    product_key, asset_type = parts[4], parts[3]
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    asset_map = {
        'text': {'key': 'copy_text', 'sender': query.message.reply_text, 'param': 'text'},
        'story': {'key': 'story_image', 'sender': context.bot.send_photo, 'param': 'photo'},
        'feed': {'key': 'feed_image', 'sender': context.bot.send_photo, 'param': 'photo'},
        'reels': {'key': 'reels_video', 'sender': context.bot.send_video, 'param': 'video'},
        'tags': {'key': 'hashtags', 'sender': query.message.reply_text, 'param': 'text'}
    }
    asset_info = asset_map.get(asset_type)
    content = kit_data.get(asset_info['key']) if asset_info else None
    if not content:
        await query.answer("⚠️ Ferramenta não disponível.", show_alert=True)
        return
    try:
        if 'reply_text' in str(asset_info['sender']):
            caption_map = {
                'text': '👇 *Texto para copiar e colar:*\n\n`{}`',
                'tags': '👇 *Hashtags para copiar e colar:*\n\n`{}`'
            }
            await asset_info['sender'](caption_map[asset_type].format(content), parse_mode=ParseMode.MARKDOWN)
        else:
            caption_map = {
                'story': '✅ Imagem para Stories pronta!',
                'feed': '✅ Imagem para Feed pronta!',
                'reels': '✅ Vídeo para Reels pronto!'
            }
            await asset_info['sender'](chat_id=query.message.chat.id, **{asset_info['param']: content, 'caption': caption_map[asset_type]})
        await query.answer("✅ Ferramenta enviada!")
    except Exception as e:
        logger.error(f"Erro ao enviar ativo social '{asset_type}' para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar.", show_alert=True)

async def _handle_social_actions(query, context: ContextTypes.DEFAULT_TYPE, parts: list, **kwargs):
    if len(parts) > 2 and parts[2] == 'send':
        await _send_social_kit_asset(query, context, parts)
    else:
        await _show_social_kit_menu(query, parts)

# --- Roteador Principal de Callbacks de Produtos ---
async def _handle_error(query, data: str, error: Exception):
    logger.error(f"Erro ao processar callback de produtos '{data}': {error}", exc_info=True)
    try:
        await query.edit_message_text(
            "Ocorreu um erro. Por favor, tente usar o comando /produtos novamente.",
            reply_markup=None
        )
    except TelegramError:
        pass

async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not (query and query.data):
        return
    try:
        await query.answer()
    except Exception:
        pass  # garante que o erro não quebre a execução
    action_map = {
        'main': _show_main_menu,
        'submenu': _show_individual_products_submenu,
        'show': _show_product_options,
        'send': _send_product_file,
        'pitch': _send_sales_pitch,
        'social': _handle_social_actions
    }
    try:
        parts = query.data.split('_')
        action = parts[1]
        handler = action_map.get(action)
        if handler:
            await handler(query=query, context=context, parts=parts)
        else:
            raise ValueError(f"Ação desconhecida: {action}")
    except Exception as e:
        await _handle_error(query, query.data, e)
