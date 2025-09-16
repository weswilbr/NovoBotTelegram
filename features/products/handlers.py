# NOME DO ARQUIVO: features/products/handlers.py
# Menu de produtos paginado (sem antiflood) – versão 100 % funcional

import logging
import telegram                              # ← usado para capturar BadRequest
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from .data import PRODUTOS                   # dados vindos do YAML

logger = logging.getLogger(__name__)

ITEMS_PER_PAGE = 6                           # nº de botões por página
# --------------------------------------------------------------------------- #
# /produtos – primeira página
# --------------------------------------------------------------------------- #
async def beneficiosprodutos(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /produtos: abre a página 0 do menu."""
    await send_product_menu_page(update, context, page=0)

# --------------------------------------------------------------------------- #
# Função que constrói/envia (ou edita) a página pedida
# --------------------------------------------------------------------------- #
async def send_product_menu_page(update: Update,
                                 context: ContextTypes.DEFAULT_TYPE,
                                 page: int = 0) -> None:
    query = update.callback_query

    # Verificação de produtos
    if not PRODUTOS:
        text = "⚠️ Nenhum produto foi encontrado. Verifique a configuração."
        if query:
            await query.message.edit_text(text)
        else:
            await update.message.reply_text(text)
        return

    # ---------- monta teclado ----------
    product_keys = sorted(PRODUTOS.keys())
    start, end = page * ITEMS_PER_PAGE, (page + 1) * ITEMS_PER_PAGE
    page_items = product_keys[start:end]

    keyboard, row = [], []
    for key in page_items:
        row.append(
            InlineKeyboardButton(
                PRODUTOS[key]["label"],
                callback_data=f"prod_details_{key}",
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Anterior",
                                        callback_data=f"prod_page_{page-1}"))
    if end < len(product_keys):
        nav.append(InlineKeyboardButton("Próxima ➡️",
                                        callback_data=f"prod_page_{page+1}"))
    if nav:
        keyboard.append(nav)

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Selecione um produto para ver os detalhes:"

    # ---------- envia / edita ----------
    if query:
        await query.answer()
        try:
            await query.message.edit_text(text, reply_markup=reply_markup)
        except telegram.error.BadRequest as e:
            # Evita erro “message is not modified” quando o usuário clica rápido
            if "message is not modified" not in str(e).lower():
                raise
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

# --------------------------------------------------------------------------- #
# Roteador de callbacks (prefixo 'prod_')
# --------------------------------------------------------------------------- #
async def products_callback_router(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not (query and query.data):
        return

    data = query.data

    if data.startswith("prod_page_"):
        await send_product_menu_page(update, context,
                                     page=int(data.split("_")[-1]))

    elif data.startswith("prod_details_"):
        await show_product_details(update, context,
                                   product_key=data.split("_")[-1])

    elif data.startswith("prod_media_"):
        _, _, key, media_type = data.split("_")
        await send_product_media(update, context, key, media_type)

    elif data.startswith("prod_pitch_"):
        await send_product_pitch(update, context,
                                 product_key=data.split("_")[-1])

    elif data.startswith("prod_social_"):
        await send_social_kit(update, context,
                              product_key=data.split("_")[-1])

# Alias para core/handlers.py
products_callback_handler = products_callback_router

# --------------------------------------------------------------------------- #
# Sub-funções: detalhes, mídias, pitch, social kit
# --------------------------------------------------------------------------- #
async def show_product_details(update: Update,
                               context: ContextTypes.DEFAULT_TYPE,
                               product_key: str) -> None:
    query = update.callback_query
    product = PRODUTOS.get(product_key)

    if not (product and query and query.message):
        if query:
            await query.answer("⚠️ Produto não encontrado.", show_alert=True)
        return

    caption = (
        f"Você selecionou: *{product['label']}*\n\n"
        "Escolha uma opção:"
    )

    keyboard = []
    media = product.get("media", {})

    # Botões de mídia
    media_buttons = []
    if media.get("video"):
        media_buttons.append(InlineKeyboardButton("🎬 Vídeo",
                                                  callback_data=f"prod_media_{product_key}_video"))
    if media.get("documento"):
        media_buttons.append(InlineKeyboardButton("📄 Folheto",
                                                  callback_data=f"prod_media_{product_key}_documento"))
    if media_buttons:
        keyboard.append(media_buttons)

    # Botões extras
    extra_buttons = []
    if product.get("pitch"):
        extra_buttons.append(InlineKeyboardButton("💰 Pitch Venda",
                                                  callback_data=f"prod_pitch_{product_key}"))
    if product.get("social_kit"):
        extra_buttons.append(InlineKeyboardButton("📲 Kit Social",
                                                  callback_data=f"prod_social_{product_key}"))
    if extra_buttons:
        keyboard.append(extra_buttons)

    keyboard.append([InlineKeyboardButton("⬅️ Voltar ao Menu",
                                          callback_data="prod_page_0")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_id = media.get("foto")
    if photo_id:
        await query.message.delete()
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_id,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        await query.message.edit_text(
            caption, reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

# --------------------------------------------------------------------------- #
async def send_product_media(update: Update,
                             context: ContextTypes.DEFAULT_TYPE,
                             product_key: str, media_type: str) -> None:
    query = update.callback_query
    await query.answer()

    product = PRODUTOS.get(product_key)
    chat_id = query.message.chat_id
    media_id = product.get("media", {}).get(media_type)

    if not media_id:
        await context.bot.send_message(
            chat_id, f"⚠️ Mídia '{media_type}' não encontrada."
        )
        return

    try:
        if media_type == "video":
            await context.bot.send_video(chat_id, media_id)
        else:
            await context.bot.send_document(chat_id, media_id)
    except Exception as e:
        logger.error("Erro ao enviar mídia %s/%s: %s", product_key, media_type, e)
        await context.bot.send_message(chat_id, "⚠️ Erro ao enviar a mídia.")

# --------------------------------------------------------------------------- #
async def send_product_pitch(update: Update,
                             context: ContextTypes.DEFAULT_TYPE,
                             product_key: str) -> None:
    query = update.callback_query
    await query.answer()

    pitch = PRODUTOS.get(product_key, {}).get("pitch")
    if pitch:
        await query.message.reply_text(pitch, parse_mode=ParseMode.MARKDOWN)
    else:
        await query.message.reply_text("⚠️ Pitch de venda não encontrado.")

# --------------------------------------------------------------------------- #
async def send_social_kit(update: Update,
                          context: ContextTypes.DEFAULT_TYPE,
                          product_key: str) -> None:
    query = update.callback_query
    await query.answer()

    kit = PRODUTOS.get(product_key, {}).get("social_kit")
    if not kit:
        await query.message.reply_text("⚠️ Kit de Mídias Sociais não encontrado.")
        return

    text = (
        "📲 *Kit de Mídias Sociais*\n\n"
        "*Texto Sugerido (copie e cole):*\n"
        f"`{kit.get('copy_text', 'N/A')}`\n\n"
        "*Hashtags Sugeridas (copie e cole):*\n"
        f"`{kit.get('hashtags', 'N/A')}`"
    )
    await query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# --------------------------------------------------------------------------- #
__all__ = [
    "beneficiosprodutos",
    "products_callback_router",
    "products_callback_handler",
]