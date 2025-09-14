# NOME DO ARQUIVO: features/business/planning.py
# REFACTOR: Handler para o comando /planificacao, oferecendo o plano de 90 dias.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

# --- Estrutura de Dados dos Arquivos ---
# Centralizar as informações facilita a manutenção. Para adicionar um novo formato, basta editar aqui.
PLANNING_FILES = {
    'pdf': {'label': "📄 Plano de 90 Dias (.pdf)", 'media_key': 'pdf'},
    'ppt': {'label': "📊 Plano de 90 Dias (.ppt)", 'media_key': 'ppt'}
}

def get_planning_menu() -> InlineKeyboardMarkup:
    """Gera o menu de opções de download dinamicamente."""
    # Usar um prefixo consistente (ex: 'planning_') facilita o roteamento dos callbacks.
    keyboard = [
        [InlineKeyboardButton(info['label'], callback_data=f"planning_{key}")]
        for key, info in PLANNING_FILES.items()
    ]
    return InlineKeyboardMarkup(keyboard)

@group_member_required
async def enviar_planificacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /planificacao.
    Exibe um menu para o usuário escolher o formato do plano de trabalho.
    """
    await update.message.reply_text(
        "🗓️ *Plano de Trabalho - 90 Dias*\n\n"
        "Este material é essencial para guiar seus primeiros passos e organizar suas metas. "
        "Escolha o formato que preferir:",
        reply_markup=get_planning_menu(),
        parse_mode='Markdown'
    )

async def planning_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lida com os callbacks do menu de planificação.
    Este handler deve ser registrado em main.py com o pattern='^planning_'.
    """
    query = update.callback_query
    # Responde ao callback para dar feedback ao usuário (o botão para de carregar).
    await query.answer()

    # Extrai o formato do callback_data. Ex: 'planning_pdf' -> 'pdf'
    formato = query.data.split('_', 1)[1]

    file_info = PLANNING_FILES.get(formato)
    if not file_info:
        logger.warning(f"Formato de planejamento desconhecido: {formato}")
        await query.edit_message_text("⚠️ Formato de arquivo inválido.")
        return

    documento_id = MEDIA.get('planotrabalho90dias', {}).get(file_info['media_key'])

    if not documento_id:
        logger.warning(f"ID de documento não encontrado para o planejamento: '{formato}'")
        await query.edit_message_text("⚠️ Desculpe, este arquivo não está disponível no momento.")
        return

    try:
        # Envia o documento solicitado.
        await context.bot.send_document(chat_id=query.message.chat.id, document=documento_id)
        
        # Edita a mensagem original para confirmar o envio e remover os botões.
        await query.edit_message_text(
            text=f"✅ O arquivo '{file_info['label']}' foi enviado! Verifique acima.",
            reply_markup=None # Remove o teclado inline
        )
    except TelegramError as e:
        logger.error(f"Erro ao enviar arquivo de planejamento (ID: {documento_id}): {e}")
        await query.edit_message_text(
            "⚠️ Ocorreu um erro ao enviar o arquivo. A equipe de administração já foi notificada."
        )

# NOTA PARA INTEGRAÇÃO EM main.py:
# Adicionar:
# from features.business import planning
# application.add_handler(CallbackQueryHandler(planning.planning_callback_handler, pattern='^planning_'))