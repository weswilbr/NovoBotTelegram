# NOME DO ARQUIVO: features/business/planning.py
# REFACTOR: Handler para o comando /planificacao, oferecendo o plano de 90 dias.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

async def enviar_planificacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe os botões para baixar o plano de trabalho."""
    keyboard = [
        [InlineKeyboardButton("📄 Enviar PDF", callback_data='planotrabalho90dias_pdf')],
        [InlineKeyboardButton("📊 Enviar PPT", callback_data='planotrabalho90dias_ppt')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha o formato do arquivo que deseja baixar:", reply_markup=reply_markup)

async def callback_planificacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o arquivo do plano de trabalho no formato selecionado."""
    query = update.callback_query
    formato = query.data.split('_')[-1] # 'pdf' or 'ppt'
    
    documento_id = MEDIA.get('planotrabalho90dias', {}).get(formato)
    if documento_id:
        await context.bot.send_document(chat_id=query.message.chat.id, document=documento_id)
    else:
        await query.edit_message_text("Erro: Arquivo não encontrado.")