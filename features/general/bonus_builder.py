# NOME DO ARQUIVO: features/general/bonus_builder.py
# REFACTOR: Gerencia o comando e os callbacks para o Bônus Construtor.
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import logging
from utils.anti_flood import command_rate_limit
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

@command_rate_limit
async def bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe as opções para o Bônus Construtor."""
    if not update.message:
        return

    keyboard = [
        [InlineKeyboardButton("🎥 Video Bônus Construtor", callback_data='bonusconstrutor_video1')],
        [InlineKeyboardButton("📄 Ler Guia Bônus Construtor", callback_data='bonusconstrutor_documento')],
        [InlineKeyboardButton("▶️ Assistir no Youtube", url='https://youtu.be/iyMiw0VpQ0Q')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Escolha uma opção para saber mais sobre o Bônus Construtor:',
        reply_markup=reply_markup
    )

async def callback_bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do menu do Bônus Construtor."""
    query = update.callback_query
    if not (query and query.message and context.bot):
        if query: await query.answer("Erro: A mensagem original não está mais acessível.")
        return

    await query.answer()
    chat_id = query.message.chat_id
    
    try:
        if query.data == 'bonusconstrutor_video1':
            video_id = MEDIA.get('bonusconstrutormidias', {}).get('video1')
            if video_id:
                await context.bot.send_video(chat_id=chat_id, video=video_id)
            else:
                await query.message.reply_text("⚠️ Vídeo não encontrado.")

        elif query.data == 'bonusconstrutor_documento':
            documento_id = MEDIA.get('bonusconstrutormidias', {}).get('documento')
            if documento_id:
                await context.bot.send_document(chat_id=chat_id, document=documento_id)
            else:
                await query.message.reply_text("⚠️ Documento não encontrado.")
    except Exception as e:
        logger.error(f"Erro ao processar callback {query.data}: {e}", exc_info=True)
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Ocorreu um erro ao processar sua solicitação.")