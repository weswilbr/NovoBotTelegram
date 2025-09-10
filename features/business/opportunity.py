# NOME DO ARQUIVO: features/business/opportunity.py
# REFACTOR: Gerencia o comando e os callbacks para a apresentação da oportunidade de negócio.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

@group_member_required
async def apresentacaooportunidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de opções para a apresentação da oportunidade."""
    video_urls = MEDIA.get('opportunity_video_urls', {})
    keyboard = [
        [InlineKeyboardButton("Vídeo Completo (Link) 🔗", url=video_urls.get('video_apresentacao', ''))],
        [InlineKeyboardButton("Vídeo Compacto (Link) 🔗", url=video_urls.get('link_plano_compacto', ''))],
        [InlineKeyboardButton("Vídeo Compacto (Arquivo) 💾", callback_data='apresentacao_arquivo_compacto')],
        [InlineKeyboardButton("PDF Apresentação 📄", callback_data='apresentacao_pdf_completo')],
        [InlineKeyboardButton("PowerPoint 📊", callback_data='apresentacao_ppt')],
        [InlineKeyboardButton("Por que 4Life? (Arquivo) ❓💾", callback_data='apresentacao_arquivo_porque')],
        [InlineKeyboardButton("Por que 4Life? (Link) ❓🔗", url=video_urls.get('link_por_que_4life', ''))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma opção para a apresentação:", reply_markup=reply_markup)

async def callback_apresentacao_oportunidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks de download de arquivos da apresentação."""
    query = update.callback_query
    action = query.data.split('_')[-1]
    
    file_id_map = {
        'compacto': 'arquivo_plano_compacto',
        'completo': 'plano_completo_slide',
        'ppt': 'powerpoint_apresentacao',
        'porque': 'arquivo_por_que_4life'
    }
    
    file_key = file_id_map.get(action)
    if not file_key: return

    file_id = MEDIA.get('opportunity_files', {}).get(file_key)
    if not file_id:
        await query.message.reply_text("⚠️ Arquivo não encontrado.")
        return
    
    sender = context.bot.send_video if file_key == 'arquivo_plano_compacto' else context.bot.send_document
    await sender(chat_id=query.message.chat.id, document=file_id)
    await query.message.reply_text(f"✅ Arquivo enviado, {update.effective_user.first_name}!")

