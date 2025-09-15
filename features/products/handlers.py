# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Totalmente reescrito para usar a nova estrutura de dados 'PRODUTOS'
# e com melhorias de usabilidade, como paginação.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# CORREÇÃO: Importa a variável unificada 'PRODUTOS'
from .data import PRODUTOS
from utils.anti_flood import command_rate_limit

logger = logging.getLogger(__name__)

# --- Constantes para o menu de paginação ---
ITEMS_PER_PAGE = 6

# --- Função Principal do Comando /produtos ---

@command_rate_limit
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe a primeira página do menu de produtos."""
    await send_product_menu_page(update, context, page=0)

# --- Funções de Lógica do Menu ---

async def send_product_menu_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0) -> None:
    """Envia uma página específica do menu de produtos, com botões de paginação."""
    query = update.callback_query
    
    if not PRODUTOS:
        text = "⚠️ Nenhum produto foi encontrado. Verifique a configuração."
        if query:
            await query.message.edit_text(text)
        elif update.message:
            await update.message.reply_text(text)
        return

    product_keys = sorted(PRODUTOS.keys())
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    
    page_items = product_keys[start_index:end_index]

    keyboard = []
    row = []
    for key in page_items:
        label = PRODUTOS[key]['label']
        row.append(InlineKeyboardButton(label, callback_data=f"prod_details_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Botões de navegação para paginação
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"prod_page_{page-1}"))
    if end_index < len(product_keys):
        nav_buttons.append(InlineKeyboardButton("Próxima ➡️", callback_data=f"prod_page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Selecione um produto para ver os detalhes:"

    if query:
        await query.answer()
        await query.message.edit_text(text, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)

# --- Roteador Principal de Callbacks ---

async def products_callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteia todos os callbacks que começam com 'prod_'."""
    query = update.callback_query
    if not query or not query.data:
        return

    # Rota para paginação
    if query.data.startswith("prod_page_"):
        page = int(query.data.split('_')[-1])
        await send_product_menu_page(update, context, page=page)

    # Rota para detalhes de um produto
    elif query.data.startswith("prod_details_"):
        product_key = query.data.split('_')[-1]
        await show_product_details(update, context, product_key)

    # Rota para enviar mídias (vídeo, documento)
    elif query.data.startswith("prod_media_"):
        _, _, product_key, media_type = query.data.split('_')
        await send_product_media(update, context, product_key, media_type)

    # Rota para enviar o pitch de vendas
    elif query.data.startswith("prod_pitch_"):
        product_key = query.data.split('_')[-1]
        await send_product_pitch(update, context, product_key)

    # Rota para enviar o kit de mídias sociais
    elif query.data.startswith("prod_social_"):
        product_key = query.data.split('_')[-1]
        await send_social_kit(update, context, product_key)

# --- Funções Específicas dos Callbacks ---

async def show_product_details(update: Update, context: ContextTypes.DEFAULT_TYPE, product_key: str) -> None:
    """Exibe o menu de opções para um produto específico (mídia, pitch, etc.)."""
    query = update.callback_query
    product = PRODUTOS.get(product_key)

    if not (product and query and query.message):
        if query: await query.answer("⚠️ Produto não encontrado.", show_alert=True)
        return

    caption = f"Você selecionou: *{product['label']}*\n\nEscolha uma opção:"
    keyboard = []
    
    # Botões de Mídia
    media = product.get('media', {})
    media_buttons = []
    if media.get('video'):
        media_buttons.append(InlineKeyboardButton("🎬 Vídeo", callback_data=f"prod_media_{product_key}_video"))
    if media.get('documento'):
        media_buttons.append(InlineKeyboardButton("📄 Folheto", callback_data=f"prod_media_{product_key}_documento"))
    if media_buttons:
        keyboard.append(media_buttons)
    
    # Outros Botões
    other_buttons = []
    if product.get('pitch'):
        other_buttons.append(InlineKeyboardButton("💰 Pitch Venda", callback_data=f"prod_pitch_{product_key}"))
    if product.get('social_kit'):
        other_buttons.append(InlineKeyboardButton("📲 Kit Social", callback_data=f"prod_social_{product_key}"))
    if other_buttons:
        keyboard.append(other_buttons)
        
    keyboard.append([InlineKeyboardButton("⬅️ Voltar ao Menu", callback_data="prod_page_0")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    photo_id = media.get('foto')
    if photo_id:
        # Apaga a mensagem anterior (o menu) para enviar uma nova com a foto
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_id,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    else:
        await query.message.edit_text(caption, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def send_product_media(update: Update, context: ContextTypes.DEFAULT_TYPE, product_key: str, media_type: str) -> None:
    """Envia a mídia solicitada (vídeo ou documento) para o chat."""
    query = update.callback_query
    await query.answer()
    
    product = PRODUTOS.get(product_key)
    chat_id = query.message.chat_id
    media_id = product.get('media', {}).get(media_type)

    if not media_id:
        await context.bot.send_message(chat_id, f"⚠️ Mídia '{media_type}' não encontrada.")
        return

    try:
        if media_type == 'video':
            await context.bot.send_video(chat_id=chat_id, video=media_id)
        elif media_type == 'documento':
            await context.bot.send_document(chat_id=chat_id, document=media_id)
    except Exception as e:
        logger.error(f"Erro ao enviar mídia {product_key}/{media_type}: {e}")
        await context.bot.send_message(chat_id, "Ocorreu um erro ao enviar a mídia.")

async def send_product_pitch(update: Update, context: ContextTypes.DEFAULT_TYPE, product_key: str) -> None:
    """Envia o texto do pitch de vendas como uma nova mensagem."""
    query = update.callback_query
    await query.answer()
    
    pitch_text = PRODUTOS.get(product_key, {}).get('pitch')
    if pitch_text:
        await query.message.reply_text(text=pitch_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await query.message.reply_text("⚠️ Pitch de venda não encontrado.")

async def send_social_kit(update: Update, context: ContextTypes.DEFAULT_TYPE, product_key: str) -> None:
    """Formata e envia o kit de mídias sociais como uma nova mensagem."""
    query = update.callback_query
    await query.answer()
    
    social_kit = PRODUTOS.get(product_key, {}).get('social_kit')
    if not social_kit:
        await query.message.reply_text("⚠️ Kit de Mídias Sociais não encontrado.")
        return
        
    copy_text = social_kit.get('copy_text', 'N/A')
    hashtags = social_kit.get('hashtags', 'N/A')
    
    message_text = (
        f"📲 *Kit de Mídias Sociais*\n\n"
        f"*Texto Sugerido (copie e cole):*\n`{copy_text}`\n\n"
        f"*Hashtags Sugeridas (copie e cole):*\n`{hashtags}`"
    )
    
    await query.message.reply_text(text=message_text, parse_mode=ParseMode.MARKDOWN)