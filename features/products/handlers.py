# NOME DO ARQUIVO: features/products/handlers.py
# Menu de produtos em 2 colunas, sem paginação, com submenu funcional.

import logging
import telegram
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

from .data import PRODUTOS

logger = logging.getLogger(__name__)

ITEMS_PER_ROW = 2           # 2 botões por linha
MAX_PRODUCTS = 200          # limite de segurança para não explodir teclado

# --------------------------------------------------------------------------- #
# /produtos – mostra a lista completa
# --------------------------------------------------------------------------- #
async def beneficiosprodutos(update: Update,
                              context: ContextTypes.DEFAULT_TYPE) -> None:
    if not PRODUTOS:
        await update.effective_chat.send_message(
            "⚠️ Nenhum produto configurado."
        )
        return

    keyboard, row = [], []
    for idx, key in enumerate(sorted(PRODUTOS.keys())[:MAX_PRODUCTS]):
        row.append(InlineKeyboardButton(
            PRODUTOS[key]["label"],
            callback_data=f"prod_{key}"
        ))
        if (idx + 1) % ITEMS_PER_ROW == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🛍️ *Lista de Produtos*\n\nClique em um produto para ver mais opções:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# --------------------------------------------------------------------------- #
# Callback router
# --------------------------------------------------------------------------- #
async def products_callback_router(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not (query and query.data):
        return

    data = query.data
    await query.answer()                    # remove spinner imediatamente

    # abrir submenu
    if data.startswith("prod_") and data.count("_") == 1:
        await _show_submenu(query, context, data.split("_")[1])
        return

    # ações do submenu
    if data.startswith("prodvid_"):
        await _send_media(query, context, data.split("_", 1)[1], "video")
    elif data.startswith("proddoc_"):
        await _send_media(query, context, data.split("_", 1)[1], "documento")
    elif data.startswith("prodpitch_"):
        await _send_pitch(query, context, data.split("_", 1)[1])
    elif data.startswith("prodsocial_"):
        await _send_social(query, context, data.split("_", 1)[1])
    elif data == "prod_back":
        # volta ao menu principal
        await _back_to_menu(query, context)

# Mantém compatibilidade com core/handlers.py
products_callback_handler = products_callback_router

# --------------------------------------------------------------------------- #
async def _back_to_menu(query, context):
    try:
        await query.message.delete()
    except telegram.error.BadRequest:
        pass
    # chama a função de comando como se fosse /produtos
    await beneficiosprodutos(query, context)

# --------------------------------------------------------------------------- #
async def _show_submenu(query, context, key: str):
    product = PRODUTOS.get(key)
    if not product:
        await query.message.reply_text("⚠️ Produto não encontrado.")
        return

    keyboard = []
    media = product.get("media", {})

    row_media = []
    if media.get("video"):
        row_media.append(InlineKeyboardButton("🎬 Vídeo", callback_data=f"prodvid_{key}"))
    if media.get("documento"):
        row_media.append(InlineKeyboardButton("📄 Folheto", callback_data=f"proddoc_{key}"))
    if row_media:
        keyboard.append(row_media)

    row_other = []
    if product.get("pitch"):
        row_other.append(InlineKeyboardButton("💰 Pitch", callback_data=f"prodpitch_{key}"))
    if product.get("social_kit"):
        row_other.append(InlineKeyboardButton("📲 Social Kit", callback_data=f"prodsocial_{key}"))
    if row_other:
        keyboard.append(row_other)

    keyboard.append([InlineKeyboardButton("🔙 Voltar", callback_data="prod_back")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = escape_markdown(f"*{product['label']}*\n\nEscolha uma opção:", version=2)
    photo_id = media.get("foto")

    try:
        if photo_id:
            await query.message.delete()
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=photo_id,
                caption=caption,
                parse_mode='MarkdownV2',
                reply_markup=reply_markup
            )
        else:
            # tenta editar; se for mesma mensagem, ignora erro
            try:
                await query.message.edit_text(
                    caption, reply_markup=reply_markup,
                    parse_mode='MarkdownV2'
                )
            except telegram.error.BadRequest as e:
                if "message is not modified" not in str(e).lower():
                    raise
    except Exception as e:
        logger.error("Erro ao mostrar submenu de %s: %s", key, e)
        await query.message.reply_text("⚠️ Erro ao mostrar submenu.")

# --------------------------------------------------------------------------- #
async def _send_media(query, context, key: str, mtype: str):
    media_id = PRODUTOS.get(key, {}).get("media", {}).get(mtype)
    if not media_id:
        await query.message.reply_text("⚠️ Mídia não encontrada.")
        return
    try:
        if mtype == "video":
            await context.bot.send_video(query.message.chat_id, media_id)
        else:
            await context.bot.send_document(query.message.chat_id, media_id)
    except Exception as e:
        logger.error("Erro enviando %s de %s: %s", mtype, key, e)
        await query.message.reply_text("⚠️ Erro ao enviar mídia.")

# --------------------------------------------------------------------------- #
async def _send_pitch(query, context, key: str):
    pitch = PRODUTOS.get(key, {}).get("pitch")
    if pitch:
        await query.message.reply_text(pitch, parse_mode=ParseMode.MARKDOWN)
    else:
        await query.message.reply_text("⚠️ Pitch não encontrado.")

# --------------------------------------------------------------------------- #
async def _send_social(query, context, key: str):
    kit = PRODUTOS.get(key, {}).get("social_kit")
    if not kit:
        await query.message.reply_text("⚠️ Social Kit não encontrado.")
        return
    text = (
        "📲 *Kit de Mídias Sociais*\n\n"
        "*Copy sugerida:*\n"
        f"`{kit.get('copy_text', '')}`\n\n"
        "*Hashtags:*\n"
        f"`{kit.get('hashtags', '')}`"
    )
    await query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# --------------------------------------------------------------------------- #
__all__ = [
    "beneficiosprodutos",
    "products_callback_router",
    "products_callback_handler",
]