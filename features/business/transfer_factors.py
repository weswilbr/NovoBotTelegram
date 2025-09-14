# NOME DO ARQUIVO: features/business/transfer_factors.py
# REFACTOR: Handler para o comando /fatorestransferencia, com materiais educativos.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Estrutura de Dados Centralizada ---
# Centralizar os materiais em um dicionário torna a manutenção muito mais fácil.
# Para adicionar/remover um item, basta editar esta estrutura.
TRANSFER_FACTOR_ASSETS = {
    'howitworks': {'label': "🎥 Como funcionam", 'media_key': 'video1'},
    'animation': {'label': "🎥 Animação", 'media_key': 'video2'},
    '3rs': {'label': "🎥 Os 3 R's", 'media_key': 'video3'},
    'table': {'label': "📄 Tabela de Porções", 'media_key': 'table'},
    'youtube': {'label': "▶️ Vídeo no YouTube", 'url': "https://youtu.be/v-h387fXKcA"}
}

def _get_tf_menu() -> InlineKeyboardMarkup:
    """Gera o menu de opções dinamicamente a partir da estrutura de dados."""
    keyboard = []
    for key, info in TRANSFER_FACTOR_ASSETS.items():
        if 'url' in info:
            # Cria um botão de URL
            keyboard.append([InlineKeyboardButton(info['label'], url=info['url'])])
        else:
            # Cria um botão de callback para download
            keyboard.append([InlineKeyboardButton(info['label'], callback_data=f"tfactors_send_{key}")])
    return InlineKeyboardMarkup(keyboard)

@group_member_required
async def fatorestransferencia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /fatorestransferencia. Exibe o menu principal."""
    await update.message.reply_text(
        "🧬 *Aprenda sobre os Fatores de Transferência:*\n\n"
        "Escolha um dos materiais abaixo para assistir ou baixar.",
        reply_markup=_get_tf_menu(),
        parse_mode='Markdown'
    )

async def _send_tf_material(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, asset_key: str) -> None:
    """Função auxiliar para encontrar e enviar o material solicitado."""
    asset_info = TRANSFER_FACTOR_ASSETS.get(asset_key)
    if not asset_info:
        logger.warning(f"Chave de ativo desconhecida para Fatores de Transferência: {asset_key}")
        return

    # Busca as informações do arquivo (tipo e id) em MEDIA
    file_info = MEDIA.get('fatorestransf', {}).get(asset_info['media_key'])
    if not file_info or 'type' not in file_info or 'id' not in file_info:
        logger.warning(f"Informação de arquivo incompleta ou não encontrada para: {asset_info['media_key']}")
        await query.edit_message_text("⚠️ Desculpe, este material não está disponível no momento.")
        return

    media_type, media_id = file_info['type'], file_info['id']

    try:
        sender = context.bot.send_video if media_type == 'video' else context.bot.send_document
        await sender(chat_id=query.message.chat.id, document=media_id) # 'document' funciona para ambos

        await query.edit_message_text(
            text=f"✅ O material '{asset_info['label']}' foi enviado!",
            reply_markup=None # Remove o teclado
        )
    except TelegramError as e:
        logger.error(f"Erro ao enviar material de Fatores de Transferência (ID: {media_id}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao enviar o material. A equipe de administração já foi notificada."
        )

async def transfer_factors_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador para todos os callbacks que começam com 'tfactors_'."""
    query = update.callback_query
    await query.answer()

    # Ex: 'tfactors_send_howitworks' -> 'howitworks'
    asset_key = query.data.split('_')[-1]
    
    await _send_tf_material(query, context, asset_key)

# NOTA PARA INTEGRAÇÃO EM main.py:
# Adicionar:
# from features.business import transfer_factors
#
# Em register_command_handlers:
# "fatorestransferencia": transfer_factors.fatorestransferencia,
#
# Em register_callback_handlers:
# application.add_handler(CallbackQueryHandler(transfer_factors.transfer_factors_callback_handler, pattern='^tfactors_'))