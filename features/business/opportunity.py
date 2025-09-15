# NOME DO ARQUIVO: features/business/opportunity.py
# REFACTOR: Atualizado para usar a nova variável MEDIA_GERAL.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# CORREÇÃO: Importa MEDIA_GERAL em vez de MEDIA
from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

async def apresentacaooportunidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de opções para a apresentação da oportunidade."""
    if not update.message:
        return
    
    # CORREÇÃO: Usa MEDIA_GERAL
    # AVISO: Certifique-se que 'opportunity_video_urls' existe no seu general_media.yml
    video_urls = MEDIA_GERAL.get('opportunity_video_urls', {})
    
    keyboard = [
        [InlineKeyboardButton("Vídeo Completo (Link) 🔗", url=video_urls.get('video_apresentacao', ''))],
        [InlineKeyboardButton("Vídeo Compacto (Link) 🔗", url=video_urls.get('link_plano_compacto', ''))],
        [InlineKeyboardButton("Vídeo Compacto (Arquivo) 💾", callback_data='apresentacao_arquivo_compacto')],
        [InlineKeyboardButton("PDF Apresentação 📄", callback_data='apresentacao_pdf_completo')],
        [InlineKeyboardButton("PowerPoint 📊", callback_data='apresentacao_ppt')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma opção para a apresentação:", reply_markup=reply_markup)

async def callback_apresentacao_oportunidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks de download de arquivos da apresentação."""
    query = update.callback_query
    if not (query and query.data and query.message):
        return
        
    await query.answer()
    action = query.data.split('_')[-1]
    
    # Mapeamento mais claro das ações para as chaves no YML
    file_key_map = {
        'compacto': 'video_plano_compacto',
        'completo': 'pdf_plano_completo',
        'ppt': 'ppt_plano_completo'
    }
    
    file_key = file_key_map.get(action)
    if not file_key:
        return

    # CORREÇÃO: Usa MEDIA_GERAL
    # AVISO: Certifique-se que 'opportunity_files' existe no seu general_media.yml
    file_id = MEDIA_GERAL.get('opportunity_files', {}).get(file_key)
    
    if not file_id:
        await context.bot.send_message(chat_id=query.message.chat_id, text="⚠️ Arquivo não encontrado.")
        return
    
    try:
        if action == 'compacto': # Se for o vídeo
            await context.bot.send_video(chat_id=query.message.chat_id, video=file_id)
        else: # Se for PDF ou PPT
            await context.bot.send_document(chat_id=query.message.chat_id, document=file_id)
    except Exception as e:
        logger.error(f"Erro ao enviar arquivo de oportunidade '{file_key}': {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text="⚠️ Ocorreu um erro ao enviar o arquivo.")