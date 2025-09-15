# NOME DO ARQUIVO: features/business/marketing.py
# REFACTOR: Handler para o comando /marketingrede, com opções de vídeo.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

async def marketing_rede(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe opções para o vídeo de Marketing de Rede."""
    # Adicionada verificação para garantir que a mensagem existe
    if not update.message:
        logger.warning("Comando /marketingrede chamado sem um objeto de mensagem.")
        return

    keyboard = [
        [InlineKeyboardButton("🔗 Assista no YouTube", url="https://www.youtube.com/watch?v=Fkeax_D_1m0")],
        [InlineKeyboardButton("⬇️ Baixar Vídeo", callback_data="baixar_video_marketing")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📹 *Vídeo de Marketing de Rede:*\nEscolha uma das opções:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# CORREÇÃO: A função foi renomeada para garantir que o Python a encontre corretamente.
# ADICIONADO: Tratamento de erro mais robusto para evitar exceções não capturadas.
async def callback_marketing_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o vídeo de Marketing de Rede quando o botão de download é clicado."""
    query = update.callback_query
    # É uma boa prática verificar se os objetos essenciais existem.
    if not query or not update.effective_chat:
        logger.warning("callback_marketing_download foi chamado sem query ou chat.")
        return

    # Notifica o Telegram que o clique foi recebido.
    await query.answer()

    video_id = MEDIA.get("marketing_rede", {}).get("video")
    
    try:
        if video_id:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_id)
        else:
            # CORREÇÃO DE ROBUSTEZ: Usa context.bot.send_message para evitar erro
            # se a mensagem original for apagada.
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Vídeo não encontrado.")
    except TelegramError as e:
        logger.error(f"Erro em callback_marketing_download ao enviar mídia: {e}", exc_info=True)
        # Tenta notificar o usuário sobre o erro.
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Ocorreu um erro ao tentar enviar o vídeo.")
        except Exception as notify_error:
            logger.error(f"Falha ao notificar o usuário sobre o erro em callback_marketing_download: {notify_error}")

