# NOME DO ARQUIVO: features/business/factory.py
# REFACTOR: Handler para o comando /fabrica4life, exibindo vídeos da fábrica.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

# Assumindo que este decorator verifica se o usuário está no grupo principal.
from utils.verification import group_member_required
# Centralize a importação de dados de mídia.
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Mapeamento de Vídeos ---
# Centraliza a busca dos IDs, tornando o código mais legível e fácil de manter.
# O uso de .get({}, {}) evita erros se a chave 'fabrica4life' não existir em MEDIA.
FACTORY_VIDEOS = {
    'armazem': MEDIA.get('fabrica4life', {}).get('armazem'),
    'envase': MEDIA.get('fabrica4life', {}).get('envase'),
    'novafabrica': MEDIA.get('fabrica4life', {}).get('novafabrica')
}

def get_factory_menu() -> InlineKeyboardMarkup:
    """Cria e retorna o menu de vídeos da fábrica."""
    # Usar um prefixo consistente (ex: 'factory_') facilita o roteamento dos callbacks.
    keyboard = [
        [InlineKeyboardButton("🏬 Armazém 4Life", callback_data='factory_armazem')],
        [InlineKeyboardButton("🏭 Envase de Produtos", callback_data='factory_envase')],
        [InlineKeyboardButton("🏗️ Nova Fábrica 4Life", callback_data='factory_novafabrica')]
    ]
    return InlineKeyboardMarkup(keyboard)

@group_member_required
async def fabrica4life(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /fabrica4life.
    Exibe um menu com opções de vídeos da fábrica.
    """
    await update.message.reply_text(
        "🏭 *Escolha um vídeo da nossa fábrica para assistir:*\n\n"
        "Selecione uma das opções abaixo e enviarei o material para você.",
        reply_markup=get_factory_menu(),
        parse_mode='Markdown'
    )

async def factory_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lida com os callbacks dos botões do menu da fábrica.
    Este handler deve ser registrado em main.py com o pattern='^factory_'.
    """
    query = update.callback_query
    # Responde ao callback imediatamente para dar feedback ao usuário (o botão para de carregar).
    await query.answer()

    # Extrai a ação do callback_data. Ex: 'factory_armazem' -> 'armazem'
    action = query.data.split('_', 1)[1]

    video_ids = FACTORY_VIDEOS.get(action)

    if not video_ids:
        logger.warning(f"ID de vídeo não encontrado para a ação da fábrica: '{action}'")
        await query.edit_message_text("⚠️ Desculpe, este vídeo não está disponível no momento.")
        return

    # Garante que 'video_ids' seja sempre uma lista para simplificar o loop.
    if not isinstance(video_ids, list):
        video_ids = [video_ids]
    
    try:
        # Envia todos os vídeos associados à ação.
        for video_id in video_ids:
            await context.bot.send_video(chat_id=query.message.chat.id, video=video_id)

        # Após o envio, edita a mensagem original para confirmar e remover os botões.
        await query.edit_message_text(
            text="✅ Vídeo(s) enviado(s) com sucesso! Confira acima.",
            reply_markup=None # Remove o teclado inline
        )

    except TelegramError as e:
        logger.error(f"Erro ao enviar vídeo da fábrica (Ação: {action}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao tentar enviar o vídeo. A equipe de administração já foi notificada."
        )

# NOTA PARA INTEGRAÇÃO EM main.py:
# O handler 'factory_callback_handler' deve ser registrado junto aos outros CallbackQueryHandlers.
# Exemplo de como adicioná-lo:
# from features.business import factory
# application.add_handler(CallbackQueryHandler(factory.factory_callback_handler, pattern='^factory_'))