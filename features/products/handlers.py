# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Gerencia o comando /produtos com um "Kit de Mídia Social" completo.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.error import TelegramError
# --- CORREÇÃO APLICADA AQUI ---
from telegram.constants import ParseMode 

from utils.verification import group_member_required
from .data import MEDIA, PITCH_DE_VENDA_TEXT

logger = logging.getLogger(__name__)

# --- Funções de Geração de Texto para os Menus ---

def _get_main_menu_text() -> str:
    return (
        "🛍️ *Menu Principal de Produtos*\n\n"
        "Navegue por nossas categorias para encontrar materiais, vídeos e informações sobre cada produto.\n\n"
        "👇 *Selecione uma opção abaixo:*"
    )

def _get_individual_submenu_text() -> str:
    return (
        "📦 *Produtos Individuais*\n\n"
        "Explore nossa linha completa de produtos. Clique em um item para ver fotos, vídeos e materiais de venda."
    )

def _get_product_options_text(product_key: str) -> str:
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    return f"Você selecionou: *{product_label}*\n\nO que você gostaria de ver sobre este produto?"


# --- Funções de Geração de Menu (Dinâmicas) ---

def _get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')]]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
    buttons, row = [], []
    for key, data in MEDIA.get('produtos', {}).items():
        row.append(InlineKeyboardButton(data.get('label', key.capitalize()), callback_data=f'products_show_{key}'))
        if len(row) == 2: buttons.append(row); row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Voltar ao Menu Principal", callback_data='products_main')])
    return InlineKeyboardMarkup(buttons)

def _get_product_options_menu(product_key: str) -> InlineKeyboardMarkup:
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
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    buttons = []
    if kit_data.get('copy_text'): buttons.append(InlineKeyboardButton("📝 Texto p/ Copiar", callback_data=f"products_social_send_text_{product_key}"))
    if kit_data.get('story_image'): buttons.append(InlineKeyboardButton("🖼️ Imagem p/ Stories", callback_data=f"products_social_send_story_{product_key}"))
    if kit_data.get('hashtags'): buttons.append(InlineKeyboardButton("#️⃣ Hashtags", callback_data=f"products_social_send_tags_{product_key}"))
    if kit_data.get('carousel_images'): buttons.append(InlineKeyboardButton("🎠 Carrossel", callback_data=f"products_social_send_carousel_{product_key}"))
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton(f"🔙 Voltar para o Produto", callback_data=f"products_show_{product_key}")])
    return InlineKeyboardMarkup(keyboard)

# --- Funções de Lógica e Handlers ---
@group_member_required
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (restante do código, sem alterações)...
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
    text = _get_individual_submenu_text()
    reply_markup = _get_individual_products_submenu()
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _show_product_options(query: Update.callback_query, product_key: str) -> None:
    text = _get_product_options_text(product_key)
    reply_markup = _get_product_options_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_product_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, file_type: str) -> None:
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
        
async def _show_social_kit_menu(query: Update.callback_query, product_key: str) -> None:
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    text = (
        f"📲 *Kit de Mídia Social para: {product_label}*\n\n"
        "Use estas ferramentas para impulsionar suas vendas nas redes sociais!"
    )
    reply_markup = _get_social_kit_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_social_kit_asset(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, asset_type: str):
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    try:
        content = None
        if asset_type == 'text':
            content = kit_data.get('copy_text')
            await query.message.reply_text(f"👇 *Texto para copiar e colar:*\n\n`{content}`", parse_mode=ParseMode.MARKDOWN)
        elif asset_type == 'story':
            content = kit_data.get('story_image')
            await context.bot.send_photo(query.message.chat_id, content, caption="✅ Imagem para Stories pronta para usar!")
        elif asset_type == 'tags':
            content = kit_data.get('hashtags')
            await query.message.reply_text(f"👇 *Hashtags para copiar e colar:*\n\n`{content}`", parse_mode=ParseMode.MARKDOWN)
        elif asset_type == 'carousel':
            content = kit_data.get('carousel_images', [])
            if content and isinstance(content, list) and all(content):
                media_group = [InputMediaPhoto(media=file_id) for file_id in content]
                await context.bot.send_media_group(query.message.chat_id, media=media_group)
            else:
                await query.answer("🎠 Carrossel de imagens ainda não disponível para este produto.", show_alert=True)
                return
        await query.answer("✅ Ferramenta enviada!")
    except TelegramError as e:
        logger.error(f"Erro ao enviar ativo social '{asset_type}' para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o material.", show_alert=True)

async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    try:
        data = query.data
        parts = data.split('_')
        action = parts[1]
        if action == 'main': await beneficiosprodutos(update, context)
        elif action == 'submenu': await _show_individual_products_submenu(query)
        elif action == 'show': await _show_product_options(query, parts[2])
        elif action == 'send': await _send_product_file(query, context, parts[2], parts[3])
        elif action == 'pitch': await _send_sales_pitch(query, parts[2])
        elif action == 'social':
            if parts[2] == 'send':
                await _send_social_kit_asset(query, context, parts[4], parts[3])
            else:
                await _show_social_kit_menu(query, parts[2])
    except (IndexError, TelegramError) as e:
        logger.error(f"Erro ao processar callback de produtos '{query.data}': {e}")
        try:
            await query.edit_message_text("Ocorreu um erro, te redirecionando para o menu principal.", reply_markup=_get_main_menu())
        except TelegramError:
            pass