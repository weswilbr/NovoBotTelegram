# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Gerencia o comando /produtos com um "Kit de Mídia Social" completo.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from .data import MEDIA, PITCH_DE_VENDA_TEXT

logger = logging.getLogger(__name__)

# --- Funções de Geração de Menu (Dinâmicas) ---

def _get_main_menu() -> InlineKeyboardMarkup:
    # ... (código existente, sem alterações)
    keyboard = [[InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')]]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
    # ... (código existente, sem alterações)
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
    # Botões existentes
    if product_data.get('foto'): buttons.append(InlineKeyboardButton("📷 Ver Foto", callback_data=f"products_send_{product_key}_foto"))
    if product_data.get('video'): buttons.append(InlineKeyboardButton("🎥 Ver Vídeo", callback_data=f"products_send_{product_key}_video"))
    if product_data.get('documento'): buttons.append(InlineKeyboardButton("📄 Ver Documento", callback_data=f"products_send_{product_key}_documento"))
    if PITCH_DE_VENDA_TEXT.get(product_key): buttons.append(InlineKeyboardButton("📝 Pitch de Venda", callback_data=f"products_pitch_{product_key}"))
    
    # --- NOVO BOTÃO PODEROSO ---
    if product_data.get('social_kit'):
        buttons.append(InlineKeyboardButton("📲 Kit de Mídia Social", callback_data=f"products_social_{product_key}"))

    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Voltar para a Lista", callback_data='products_submenu_individual')])
    return InlineKeyboardMarkup(keyboard)

def _get_social_kit_menu(product_key: str) -> InlineKeyboardMarkup:
    """Cria o menu de opções para o Kit de Mídia Social."""
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

# (beneficiosprodutos, _show_individual_products_submenu, _show_product_options, _send_product_file, _send_sales_pitch)
# As funções existentes permanecem as mesmas que na versão "enfeitada".

# --- NOVAS Funções para o Kit de Mídia Social ---

async def _show_social_kit_menu(query: Update.callback_query, product_key: str) -> None:
    """Exibe o menu de ferramentas do Kit de Mídia Social."""
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    text = (
        f"📲 *Kit de Mídia Social para: {product_label}*\n\n"
        "Use estas ferramentas para impulsionar suas vendas nas redes sociais!"
    )
    reply_markup = _get_social_kit_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def _send_social_kit_asset(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, asset_type: str):
    """Envia um ativo específico do kit de mídia social."""
    kit_data = MEDIA.get('produtos', {}).get(product_key, {}).get('social_kit', {})
    
    try:
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
            media_group = [InputMediaPhoto(media=file_id) for file_id in content]
            if media_group:
                await context.bot.send_media_group(query.message.chat_id, media=media_group)
        
        await query.answer("✅ Ferramenta enviada!")

    except TelegramError as e:
        logger.error(f"Erro ao enviar ativo social '{asset_type}' para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o material.", show_alert=True)

# --- Roteador Principal ---

async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador inteligente para todos os callbacks de produtos."""
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
        
        # --- NOVAS ROTAS ---
        elif action == 'social':
            # Se for uma ação dentro do kit social (ex: products_social_send_text_...)
            if parts[2] == 'send':
                await _send_social_kit_asset(query, context, parts[4], parts[3])
            # Se for para abrir o menu do kit social (ex: products_social_riovidaburst)
            else:
                await _show_social_kit_menu(query, parts[2])
                
    except (IndexError, TelegramError) as e:
        logger.error(f"Erro ao processar callback de produtos '{query.data}': {e}")