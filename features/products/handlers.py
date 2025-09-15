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
    """Retorna o texto para o menu principal de produtos."""
    return "🛍️ *Menu Principal de Produtos*\n\nNavegue por nossas categorias para encontrar materiais e ferramentas de marketing para cada produto."

def _get_individual_submenu_text() -> str:
    """Retorna o texto para o submenu de produtos individuais."""
    return "📦 *Produtos Individuais*\n\nSelecione um produto para ver os detalhes e acessar seu kit de marketing."

def _get_product_options_text(product_key: str) -> str:
    """Retorna o texto de opções para um produto específico."""
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    return f"Você selecionou: *{product_label}*\n\nO que você gostaria de ver ou usar?"

# --- Funções de Geração de Menu (Inline Keyboards) ---
def _get_main_menu() -> InlineKeyboardMarkup:
    """Cria o teclado para o menu principal."""
    keyboard = [[InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')]]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
    """Cria o teclado com a lista de todos os produtos individuais."""
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
    """Cria o teclado de opções para um produto específico (foto, vídeo, etc.)."""
    product_data = MEDIA.get('produtos', {}).get(product_key, {})
    buttons = []
    if product_data.get('foto'): buttons.append(InlineKeyboardButton("📷 Ver Foto", callback_data=f"products_send_{product_key}_foto"))
    if product_data.get('video'): buttons.append(InlineKeyboardButton("🎥 Ver Vídeo", callback_data=f"products_send_{product_key}_video"))
    if product_data.get('documento'): buttons.append(InlineKeyboardButton("📄 Ver Documento", callback_data=f"products_send_{product_key}_documento"))
    if PITCH_DE_VENDA_TEXT.get(product_key): buttons.append(InlineKeyboardButton("📝 Pitch de Venda", callback_data=f"products_pitch_{product_key}"))
    if product_data.get('social_kit'):
        buttons.append(InlineKeyboardButton("📲 Kit de Mídia Social", callback_data=f"products_social_{product_key}"))
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Voltar para a Lista", callback_data='products_submenu_individual')])
    return InlineKeyboardMarkup(keyboard)

def _get_social_kit_menu(product_key: str) -> InlineKeyboardMarkup:
    """Cria o teclado de opções para o Kit de Mídia Social."""
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    buttons = []
    if kit_data.get('copy_text'): buttons.append(InlineKeyboardButton("📝 Texto p/ Post", callback_data=f"products_social_send_text_{product_key}"))
    if kit_data.get('story_image'): buttons.append(InlineKeyboardButton("🖼️ Imagem p/ Stories", callback_data=f"products_social_send_story_{product_key}"))
    if kit_data.get('feed_image'): buttons.append(InlineKeyboardButton("🏞️ Imagem p/ Feed", callback_data=f"products_social_send_feed_{product_key}"))
    if kit_data.get('reels_video'): buttons.append(InlineKeyboardButton("🎬 Vídeo p/ Reels", callback_data=f"products_social_send_reels_{product_key}"))
    if kit_data.get('hashtags'): buttons.append(InlineKeyboardButton("#️⃣ Hashtags", callback_data=f"products_social_send_tags_{product_key}"))
    
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton(f"🔙 Voltar para o Produto", callback_data=f"products_show_{product_key}")])
    return InlineKeyboardMarkup(keyboard)

# --- Handlers de Lógica ---
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /produtos. Envia o menu principal."""
    if not update.message:
        return
    text = _get_main_menu_text()
    reply_markup = _get_main_menu()
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _show_main_menu(query: Update.callback_query) -> None:
    """Edita a mensagem para mostrar o menu principal (usado pelo botão 'Voltar')."""
    text = _get_main_menu_text()
    reply_markup = _get_main_menu()
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        if "message is not modified" not in str(e).lower():
            logger.warning(f"Erro ao editar para o menu principal: {e}")

async def _show_individual_products_submenu(query: Update.callback_query) -> None:
    """Mostra a lista de produtos individuais."""
    text = _get_individual_submenu_text()
    reply_markup = _get_individual_products_submenu()
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _show_product_options(query: Update.callback_query, product_key: str) -> None:
    """Mostra as opções para um produto específico."""
    text = _get_product_options_text(product_key)
    reply_markup = _get_product_options_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_product_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, file_type: str) -> None:
    """Envia um arquivo de mídia (foto, vídeo, documento) do produto."""
    file_id = MEDIA.get('produtos', {}).get(product_key, {}).get(file_type)
    if not file_id:
        await query.answer("⚠️ Mídia não encontrada.", show_alert=True)
        return
    try:
        sender_map = {'foto': context.bot.send_photo, 'video': context.bot.send_video, 'documento': context.bot.send_document}
        await sender_map[file_type](chat_id=query.message.chat_id, **{file_type: file_id})
        await query.edit_message_text(f"✅ Material enviado!\n\nUse /produtos para voltar ao menu.", reply_markup=None)
    except (TelegramError, KeyError) as e:
        logger.error(f"Erro ao enviar arquivo '{file_type}' para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar a mídia.", show_alert=True)

async def _send_sales_pitch(query: Update.callback_query, product_key: str) -> None:
    """Envia o texto do pitch de vendas para um produto."""
    pitch_text = PITCH_DE_VENDA_TEXT.get(product_key)
    if not pitch_text:
        await query.answer("⚠️ Pitch de venda não encontrado.", show_alert=True)
        return
    try:
        await query.message.reply_text(pitch_text, parse_mode=ParseMode.MARKDOWN)
        await query.edit_message_text("✅ Pitch de venda enviado!\n\nUse /produtos para voltar ao menu.", reply_markup=None)
    except TelegramError as e:
        logger.error(f"Erro ao enviar pitch de venda para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o texto.", show_alert=True)
        
async def _show_social_kit_menu(query: Update.callback_query, product_key: str) -> None:
    """Mostra o menu do Kit de Mídia Social."""
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    text = f"📲 *Kit de Mídia Social: {product_label}*\n\nUse estas ferramentas para impulsionar suas vendas!"
    reply_markup = _get_social_kit_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_social_kit_asset(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, asset_type: str):
    """Envia um item específico do Kit de Mídia Social (texto, imagem, etc.)."""
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    
    asset_map = {
        'text': {'key': 'copy_text', 'sender': 'reply_text', 'caption': '👇 *Texto para copiar e colar:*\n\n`{}`'},
        'story': {'key': 'story_image', 'sender': 'send_photo', 'caption': '✅ Imagem para Stories pronta para usar!'},
        'feed': {'key': 'feed_image', 'sender': 'send_photo', 'caption': '✅ Imagem para Feed pronta para usar!'},
        'reels': {'key': 'reels_video', 'sender': 'send_video', 'caption': '✅ Vídeo para Reels pronto para usar!'},
        'tags': {'key': 'hashtags', 'sender': 'reply_text', 'caption': '👇 *Hashtags para copiar e colar:*\n\n`{}`'}
    }
    
    asset_info = asset_map.get(asset_type)
    if not asset_info or not kit_data.get(asset_info['key']):
        await query.answer("⚠️ Ferramenta não disponível para este produto.", show_alert=True)
        return
        
    content = kit_data.get(asset_info['key'])
    
    try:
        if asset_info['sender'] == 'reply_text':
             await query.message.reply_text(asset_info['caption'].format(content), parse_mode=ParseMode.MARKDOWN)
        else:
             sender_method = getattr(context.bot, asset_info['sender'])
             # O parâmetro para enviar mídia pode ser 'photo', 'video', etc.
             media_param = asset_info['sender'].replace('send_', '')
             await sender_method(chat_id=query.message.chat_id, **{media_param: content, 'caption': asset_info['caption']})
        
        await query.answer("✅ Ferramenta enviada!")
    except Exception as e:
        logger.error(f"Erro ao enviar ativo social '{asset_type}' para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o material.", show_alert=True)

# --- Roteador Principal de Callbacks de Produtos ---
async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteia todas as ações de callback que começam com 'products_'."""
    query = update.callback_query
    if not query:
        return
        
    await query.answer()
    try:
        data = query.data
        parts = data.split('_')
        action = parts[1]
        
        if action == 'main': 
            await _show_main_menu(query)
        elif action == 'submenu': 
            await _show_individual_products_submenu(query)
        elif action == 'show': 
            await _show_product_options(query, parts[2])
        elif action == 'send': 
            await _send_product_file(query, context, parts[2], parts[3])
        elif action == 'pitch': 
            await _send_sales_pitch(query, parts[2])
        elif action == 'social':
            if len(parts) > 2 and parts[2] == 'send':
                await _send_social_kit_asset(query, context, parts[4], parts[3])
            else:
                await _show_social_kit_menu(query, parts[2])
    except Exception as e:
        logger.error(f"Erro ao processar callback de produtos '{query.data}': {e}", exc_info=True)
        try:
            await query.edit_message_text(
                "Ocorreu um erro ao processar sua solicitação. Tente usar o comando /produtos novamente.",
                reply_markup=None
            )
        except TelegramError:
            pass

