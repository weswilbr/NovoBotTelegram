# NOME DO ARQUIVO: features/community/loyalty.py
# REFACTOR: Handler para o comando /fidelidade, com informações do programa de fidelidade.
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from features.products.data import MEDIA

YOUTUBE_URL = "https://youtu.be/f7bvrk7hh3U?si=-3PLes7BRFBcKPHY"

async def fidelidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o menu do programa de fidelidade."""
    keyboard = [
        [InlineKeyboardButton("▶️ Assistir no YouTube", url=YOUTUBE_URL)],
        [InlineKeyboardButton("⬇️ Baixar Vídeo", callback_data='fidelidade_download')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💎 *Programa de Fidelidade 4Life*\n\nEscolha uma opção:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def callback_fidelidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com o callback de download do vídeo de fidelidade."""
    query = update.callback_query
    if query.data == 'fidelidade_download':
        video_id = MEDIA['fidelidade'].get('video')
        if video_id:
            await context.bot.send_video(chat_id=query.message.chat.id, video=video_id)
        else:
            await query.message.reply_text("⚠️ Vídeo não encontrado.")

