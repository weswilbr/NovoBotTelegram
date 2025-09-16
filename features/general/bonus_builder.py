# NOME DO ARQUIVO: features/general/bonus_builder.py
# Menu “Construtor de Bônus” – versão sem erro de Markdown e com prefixo correto.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# /bonusconstrutor – mostra o menu principal
# --------------------------------------------------------------------------- #
async def bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando que exibe o menu do Construtor de Bônus."""
    if not update.message:
        return

    keyboard = _main_keyboard()

    # Sem parse_mode para evitar BadRequest “can’t parse entities”
    await update.message.reply_text(
        "🔢 Construtor de Bônus\n\nEscolha uma opção abaixo:",
        reply_markup=keyboard,
    )

# --------------------------------------------------------------------------- #
# Callback router
# --------------------------------------------------------------------------- #
async def callback_bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteia botões prefixados com 'bonusconstrutor_'."""
    query = update.callback_query
    if not (query and query.data):
        return

    data = query.data
    await query.answer()                 # remove spinner

    if data == "bonusconstrutor_pdf":
        await _send_pdf(query, context)
    elif data == "bonusconstrutor_video":
        await _send_video(query, context)

# --------------------------------------------------------------------------- #
# Teclado principal
# --------------------------------------------------------------------------- #
def _main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📄 PDF", callback_data="bonusconstrutor_pdf"),
            InlineKeyboardButton("🎬 Vídeo", callback_data="bonusconstrutor_video"),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

# --------------------------------------------------------------------------- #
# Funções auxiliares
# --------------------------------------------------------------------------- #
async def _send_pdf(query, context):
    file_id = MEDIA_GERAL.get("bonusconstrutormidias", {}).get("documento")
    if file_id:
        await context.bot.send_document(query.message.chat_id, file_id)
    else:
        await query.message.reply_text("⚠️ PDF não encontrado.")

async def _send_video(query, context):
    video_id = MEDIA_GERAL.get("bonusconstrutormidias", {}).get("video1")
    if video_id:
        await context.bot.send_video(query.message.chat_id, video_id)
    else:
        await query.message.reply_text("⚠️ Vídeo não encontrado.")

# --------------------------------------------------------------------------- #
# Exports
# --------------------------------------------------------------------------- #
__all__ = [
    "bonus_construtor",
    "callback_bonus_construtor",
]