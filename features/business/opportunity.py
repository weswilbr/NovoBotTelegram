# NOME DO ARQUIVO: features/business/opportunity.py
# REFACTOR: Gerencia o comando e os callbacks para a apresentação da oportunidade de negócio.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Estrutura de Dados Centralizada ---
# Centralizar os "ativos" (links e arquivos) em um único local torna a manutenção muito mais fácil.
# Para adicionar um novo item ao menu, basta adicioná-lo a este dicionário.
OPPORTUNITY_ASSETS = {
    # Itens que são links externos
    'urls': [
        {'label': "Vídeo Completo (Link) 🔗", 'key': 'video_apresentacao'},
        {'label': "Vídeo Compacto (Link) 🔗", 'key': 'link_plano_compacto'},
        {'label': "Por que 4Life? (Link) ❓🔗", 'key': 'link_por_que_4life'}
    ],
    # Itens que são arquivos para download
    'files': [
        {'label': "Vídeo Compacto (Arquivo) 💾", 'action': 'compacto', 'media_key': 'arquivo_plano_compacto', 'type': 'video'},
        {'label': "PDF Apresentação 📄", 'action': 'pdf', 'media_key': 'plano_completo_slide', 'type': 'document'},
        {'label': "PowerPoint 📊", 'action': 'ppt', 'media_key': 'powerpoint_apresentacao', 'type': 'document'},
        {'label': "Por que 4Life? (Arquivo) ❓💾", 'action': 'porque', 'media_key': 'arquivo_por_que_4life', 'type': 'video'}
    ]
}

def get_opportunity_menu() -> InlineKeyboardMarkup:
    """Gera o teclado de opções dinamicamente a partir da estrutura de dados."""
    keyboard = []
    video_urls = MEDIA.get('opportunity_video_urls', {})

    # Adiciona os botões de URL
    for item in OPPORTUNITY_ASSETS['urls']:
        url = video_urls.get(item['key'])
        if url: # Só adiciona o botão se a URL existir
            keyboard.append([InlineKeyboardButton(item['label'], url=url)])

    # Adiciona os botões de callback para download
    for item in OPPORTUNITY_ASSETS['files']:
        callback_data = f"opportunity_download_{item['action']}"
        keyboard.append([InlineKeyboardButton(item['label'], callback_data=callback_data)])
        
    return InlineKeyboardMarkup(keyboard)

@group_member_required
async def apresentacaooportunidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /apresentacao. Exibe o menu de opções."""
    await update.message.reply_text(
        "💼 *Apresentação da Oportunidade*\n\n"
        "Escolha um dos materiais abaixo para visualizar ou baixar:",
        reply_markup=get_opportunity_menu(),
        parse_mode='Markdown'
    )

async def _send_opportunity_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, action: str) -> None:
    """Função auxiliar para encontrar e enviar o arquivo solicitado."""
    # Encontra o item correspondente na nossa estrutura de dados
    asset_to_send = next((item for item in OPPORTUNITY_ASSETS['files'] if item['action'] == action), None)
    
    if not asset_to_send:
        logger.warning(f"Ação de oportunidade desconhecida: {action}")
        await query.edit_message_text("⚠️ Ação inválida. Por favor, tente novamente.")
        return

    # Busca o ID do arquivo em MEDIA
    file_id = MEDIA.get('opportunity_files', {}).get(asset_to_send['media_key'])

    if not file_id:
        logger.warning(f"ID de arquivo não encontrado para oportunidade: {asset_to_send['media_key']}")
        await query.edit_message_text("⚠️ Desculpe, este arquivo não está disponível no momento.")
        return

    try:
        # Escolhe a função de envio correta (send_video ou send_document)
        sender = context.bot.send_video if asset_to_send['type'] == 'video' else context.bot.send_document
        await sender(chat_id=query.message.chat.id, document=file_id) # 'document' funciona para ambos
        
        # Edita a mensagem original para confirmar e remover os botões
        await query.edit_message_text(
            f"✅ Arquivo '{asset_to_send['label'].split('(')[0].strip()}' enviado!",
            reply_markup=None
        )
    except TelegramError as e:
        logger.error(f"Erro ao enviar arquivo de oportunidade (ID: {file_id}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao enviar o arquivo. A equipe de administração já foi notificada."
        )


async def opportunity_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador para todos os callbacks que começam com 'opportunity_'."""
    query = update.callback_query
    await query.answer()

    # Extrai a ação do callback. Ex: 'opportunity_download_pdf' -> 'pdf'
    action = query.data.split('_')[-1]
    
    await _send_opportunity_file(query, context, action)

# NOTA PARA INTEGRAÇÃO EM main.py:
# Adicionar:
# from features.business import opportunity
# application.add_handler(CallbackQueryHandler(opportunity.opportunity_callback_handler, pattern='^opportunity_'))