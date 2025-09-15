# NOME DO ARQUIVO: features/business/factory.py
# REFACTOR: Atualizado para usar a nova variável MEDIA_GERAL.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# CORREÇÃO: Importa MEDIA_GERAL em vez de MEDIA
from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

async def fabrica4life(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de vídeos da Fábrica 4Life."""
    if not update.message:
        return
        
    keyboard = [
        [InlineKeyboardButton("🏬 Armazém 4Life", callback_data='fabrica_armazem')],
        [InlineKeyboardButton("🏭 Envase de Produtos", callback_data='fabrica_envase')],
        # [InlineKeyboardButton("🏗️ Nova Fábrica 4Life", callback_data='fabrica_novafabrica')] # Descomente se existir nos dados
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🏭 *Escolha um vídeo para visualizar:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def callback_fabrica4life(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do menu da fábrica de forma segura."""
    query = update.callback_query
    if not (query and query.data and query.message):
        return
    
    await query.answer()
    action = query.data.split('_')[1]

    # CORREÇÃO: Usa MEDIA_GERAL e .get() para segurança
    video_id = MEDIA_GERAL.get('fabrica4life', {}).get(action)
    
    if not video_id:
        await context.bot.send_message(chat_id=query.message.chat_id, text="⚠️ Vídeo não encontrado.")
        return

    try:
        await context.bot.send_video(chat_id=query.message.chat_id, video=video_id)
    except Exception as e:
        logger.error(f"Erro ao enviar vídeo da fábrica '{action}': {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text="⚠️ Ocorreu um erro ao enviar o vídeo.")