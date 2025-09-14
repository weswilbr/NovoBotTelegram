# NOME DO ARQUIVO: features/general/bonus_builder.py
# REFACTOR: Gerencia o comando e os callbacks para o Bônus Construtor.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from utils.anti_flood import command_rate_limit
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Estrutura de Dados Centralizada ---
# Centralizar os materiais em um dicionário torna a manutenção muito mais fácil.
# Para adicionar/remover um item, basta editar esta estrutura.
BUILDER_ASSETS = {
    'video': {'label': "🎥 Vídeo Bônus Construtor", 'media_key': 'video1', 'type': 'video'},
    'document': {'label': "📄 Ler Guia Bônus Construtor", 'media_key': 'documento', 'type': 'document'},
    'youtube': {'label': "▶️ Assistir no Youtube", 'url': 'https://youtu.be/iyMiw0VpQ0Q'}
}

def _get_bonus_builder_menu() -> InlineKeyboardMarkup:
    """Gera o menu de opções dinamicamente a partir da estrutura de dados."""
    keyboard = []
    for key, info in BUILDER_ASSETS.items():
        if 'url' in info:
            keyboard.append([InlineKeyboardButton(info['label'], url=info['url'])])
        else:
            # Padroniza o callback_data para facilitar o roteamento.
            keyboard.append([InlineKeyboardButton(info['label'], callback_data=f"bbuilder_send_{key}")])
    return InlineKeyboardMarkup(keyboard)

@group_member_required
@command_rate_limit
async def bonus_construtor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /bonusconstrutor.
    Exibe um menu com materiais sobre o Bônus Construtor.
    """
    if not update.message:
        return

    await update.message.reply_text(
        '🏆 *Bônus Construtor*\n\n'
        'Aprenda como estruturar sua equipe para ganhar este bônus todos os meses! '
        'Escolha uma opção abaixo:',
        reply_markup=_get_bonus_builder_menu(),
        parse_mode='Markdown'
    )

async def _send_builder_asset(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, asset_key: str) -> None:
    """Função auxiliar para encontrar e enviar o material do Bônus Construtor."""
    asset_info = BUILDER_ASSETS.get(asset_key)
    if not asset_info:
        logger.warning(f"Chave de ativo desconhecida para Bônus Construtor: {asset_key}")
        return

    media_id = MEDIA.get('bonusconstrutormidias', {}).get(asset_info['media_key'])

    if not media_id:
        logger.warning(f"ID de mídia não encontrado para: {asset_info['media_key']}")
        await query.edit_message_text("⚠️ Desculpe, este material não está disponível no momento.")
        return

    try:
        sender = context.bot.send_video if asset_info['type'] == 'video' else context.bot.send_document
        await sender(chat_id=query.message.chat.id, document=media_id)

        # Edita a mensagem original para confirmar o envio e remover os botões (melhor UX).
        await query.edit_message_text(
            text=f"✅ O material '{asset_info['label']}' foi enviado!",
            reply_markup=None
        )
    except TelegramError as e:
        logger.error(f"Erro ao enviar material do Bônus Construtor (ID: {media_id}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao enviar o material. A equipe de administração já foi notificada."
        )

async def bonus_builder_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Roteador para todos os callbacks que começam com 'bbuilder_'.
    """
    query = update.callback_query
    if not query:
        return

    await query.answer()

    # Extrai a chave do ativo. Ex: 'bbuilder_send_video' -> 'video'
    asset_key = query.data.split('_')[-1]
    
    await _send_builder_asset(query, context, asset_key)

# NOTA PARA INTEGRAÇÃO EM main.py e core/handlers.py:
#
# 1. Em main.py, o comando já está correto:
#    "bonusconstrutor": bonus_builder.bonus_construtor,
#
# 2. Em core/handlers.py, a rota antiga deve ser substituída pela nova:
#    DE:
#    'bonusconstrutor_': callback_bonus_construtor,
#
#    PARA:
#    elif data.startswith('bbuilder_'):
#        await bonus_builder.bonus_builder_callback_handler(update, context)