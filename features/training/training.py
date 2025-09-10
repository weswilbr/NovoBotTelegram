# NOME DO ARQUIVO: features/training/training.py
# REFACTOR: Gerencia a lógica para exibir os materiais de treinamento.

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ContextTypes

from utils.verification import group_member_required
import logging

logger = logging.getLogger(__name__)

# --- Dados dos Materiais ---
# Os dados foram movidos para este arquivo para torná-lo autossuficiente.
TRAINING_MATERIALS = {
    'apoio': [
        {"title": "📄 Manejo de Objeções", "file_id": 'BQACAgEAAxkBAAIqn2cte9Hbg1Vdy8_Q7F-h6kLYmdHrAAJOBAACbpZxRd1zqTq38VfqNgQ'},
        {"title": "📄 Cuidados e Gerenciamento de clientes", "file_id": 'BQACAgEAAxkBAAIrr2cvKhYe8LiuttRymHqhZ6NLLQdkAAIeBAACz_V5RdW-UNf_BNgvNgQ'},
        {"title": "📄 Tipo de Fechamento - Lina Maria", "file_id": 'BQACAgEAAxkBAAIqo2cte-bTPo54-I7KXtuas4-dO5KtAAJQBAACbpZxRYdOZc1JPX07NgQ'}
    ],
    'tutoriais': [
        {"title": "🎥 Simular Preço Produto no APP", "file_id": 'BAACAgEAAxkBAAIxwmc496iu0IrH4dWbBYoJHaxdhotiAALkBAACQgPJRfVaqctZ8xXNNgQ'}
    ]
}

# --- Handlers ---

@group_member_required
async def treinamento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal de treinamento."""
    keyboard = [
        [InlineKeyboardButton("🛠️ Material da Academia de Platinos", callback_data='apoio')],
        [InlineKeyboardButton("🎥 Tutoriais", callback_data='tutoriais')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    target_message = update.message or (update.callback_query and update.callback_query.message)
    if not target_message:
        logger.warning("Função 'treinamento' chamada sem um alvo de mensagem válido.")
        return

    try:
        if update.message:
            await target_message.reply_text("Escolha um treinamento:", reply_markup=reply_markup)
        elif update.callback_query:
            await target_message.edit_text("Escolha um treinamento:", reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Erro ao enviar ou editar menu de treinamento: {e}")

@group_member_required
async def handle_treinamento_callback(update: Update, context: CallbackContext):
    """Lida com os cliques nos botões de treinamento."""
    query = update.callback_query
    if not (query and query.data and query.message):
        return
        
    user_mention = f"@{query.from_user.username}" if query.from_user.username else query.from_user.first_name
    await query.answer()

    callback_data = query.data

    try:
        if callback_data == 'apoio' or callback_data == 'tutoriais':
            materials = TRAINING_MATERIALS.get(callback_data, [])
            buttons = [
                [InlineKeyboardButton(material['title'], callback_data=f"{callback_data}_{index}")]
                for index, material in enumerate(materials)
            ]
            buttons.append([InlineKeyboardButton("⬅️ Voltar", callback_data='voltar')])
            reply_markup = InlineKeyboardMarkup(buttons)
            
            text = f"{user_mention}, selecione o material de apoio:" if callback_data == 'apoio' else f"{user_mention}, selecione um tutorial:"
            await query.edit_message_text(text=text, reply_markup=reply_markup)

        elif callback_data.startswith(('apoio_', 'tutoriais_')):
            try:
                material_type, index_str = callback_data.split('_', 1)
                index = int(index_str)
                selected_material = TRAINING_MATERIALS.get(material_type, [])[index]
                file_id = selected_material.get("file_id")
                title = selected_material.get("title")

                if file_id:
                    await context.bot.send_document(chat_id=query.message.chat_id, document=file_id)
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=f"{user_mention}, seu material '{title}' foi enviado! 📤"
                    )
            except (ValueError, IndexError, KeyError) as e:
                logger.error(f"Erro ao processar callback de material '{callback_data}': {e}")
                await query.message.reply_text("⚠️ Ocorreu um erro ao buscar este material.")

        elif callback_data == 'voltar':
            await treinamento(update, context)

    except Exception as e:
        logger.error(f"Erro inesperado no callback de treinamento '{callback_data}': {e}", exc_info=True)
        if query.message:
            await query.message.reply_text("⚠️ Ocorreu um erro. Por favor, tente novamente.")

