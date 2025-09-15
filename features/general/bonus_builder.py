# NOME DO ARQUIVO: features/general/bonus_builder.py
# Construtor de bônus (menu interativo)

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------- #
# Função de callback (exibida no menu principal)
# ------------------------------------------------------------------- #
async def bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /bonusconstrutor – mostra quadro de bônus e botões."""
    if not update.message:
        return

    await update.message.reply_text(
        "🔢 *Construtor de Bônus*\n\n"
        "Escolha uma opção abaixo:",
        parse_mode='Markdown',
        reply_markup=_main_keyboard()
    )

# ------------------------------------------------------------------- #
# Callback router para botões do construtor
# ------------------------------------------------------------------- #
async def callback_bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not (query and query.data):
        return

    data = query.data
    if data == "bonus_pdf":
        await _send_pdf(update, context)
    elif data == "bonus_video":
        await _send_video(update, context)

# ------------------------------------------------------------------- #
# Helpers
# ------------------------------------------------------------------- #
def _main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📄 PDF", callback_data="bonus_pdf"),
            InlineKeyboardButton("🎬 Vídeo", callback_data="bonus_video"),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

async def _send_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file_id = MEDIA_GERAL.get("bonusconstrutormidias", {}).get("documento")
    if file_id:
        await context.bot.send_document(query.message.chat_id, file_id)
    else:
        await query.message.reply_text("⚠️ PDF não encontrado.")

async def _send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    video_id = MEDIA_GERAL.get("bonusconstrutormidias", {}).get("video1")
    if video_id:
        await context.bot.send_video(query.message.chat_id, video_id)
    else:
        await query.message.reply_text("⚠️ Vídeo não encontrado.")