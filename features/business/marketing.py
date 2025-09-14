# NOME DO ARQUIVO: features/business/marketing.py
# REFACTOR: Handler para o comando /marketingrede, com opções de vídeo.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Constantes do Módulo ---
# Centralizar informações como URLs e IDs facilita a manutenção.
YOUTUBE_URL = "https://www.youtube.com/watch?v=Fkeax_D_1m0"
VIDEO_ID = MEDIA.get("marketing_rede", {}).get("video")

def get_marketing_menu() -> InlineKeyboardMarkup:
    """Cria e retorna o menu de opções para o marketing de rede."""
    # Usar um prefixo consistente (ex: 'marketing_') facilita o roteamento dos callbacks.
    keyboard = [
        [InlineKeyboardButton("🔗 Assistir no YouTube", url=YOUTUBE_URL)],
        [InlineKeyboardButton("⬇️ Baixar o Vídeo (.mp4)", callback_data="marketing_download")]
    ]
    return InlineKeyboardMarkup(keyboard)

@group_member_required
async def marketing_rede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /marketingrede.
    Exibe um menu com opções para assistir ou baixar o vídeo de marketing.
    """
    await update.message.reply_text(
        "📹 *Vídeo sobre Marketing de Rede*\n\n"
        "Este vídeo explica os conceitos fundamentais do nosso modelo de negócio. "
        "Você pode assisti-lo diretamente no YouTube ou baixá-lo para o seu dispositivo.",
        reply_markup=get_marketing_menu(),
        parse_mode='Markdown'
    )

async def marketing_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lida com os callbacks do menu de marketing.
    Este handler deve ser registrado em main.py com o pattern='^marketing_'.
    """
    query = update.callback_query
    # Responde ao callback para remover o ícone de "carregando" do botão.
    await query.answer()

    # Verifica se o ID do vídeo foi carregado corretamente.
    if not VIDEO_ID:
        logger.warning("ID do vídeo de marketing de rede não encontrado em MEDIA.")
        await query.edit_message_text(
            "⚠️ Desculpe, o arquivo de vídeo não está disponível para download no momento."
        )
        return

    try:
        # Envia o vídeo para o usuário.
        await context.bot.send_video(chat_id=query.message.chat.id, video=VIDEO_ID)
        
        # Edita a mensagem original para remover os botões e confirmar o envio.
        # Isso cria uma experiência de usuário mais limpa.
        await query.edit_message_text(
            text="✅ Vídeo enviado com sucesso! Verifique acima.",
            reply_markup=None # Remove o teclado inline
        )
    except TelegramError as e:
        logger.error(f"Erro ao enviar vídeo de marketing (ID: {VIDEO_ID}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao tentar enviar o vídeo. A equipe de administração já foi notificada."
        )

# NOTA PARA INTEGRAÇÃO EM main.py:
# O handler 'marketing_callback_handler' deve ser registrado junto aos outros CallbackQueryHandlers.
# Exemplo de como adicioná-lo:
# from features.business import marketing
# application.add_handler(CallbackQueryHandler(marketing.marketing_callback_handler, pattern='^marketing_'))