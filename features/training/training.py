# NOME DO ARQUIVO: features/training/training.py
# REFACTOR: Handler para o comando /treinamento e seus submenus.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from features.products.data import TRAINING_MATERIALS

logger = logging.getLogger(__name__)

async def treinamento(update, context):
    """Exibe o menu principal de treinamento."""
    keyboard = [
        [InlineKeyboardButton("🛠️ Material da Academia de Platinos", callback_data='apoio')],
        [InlineKeyboardButton("🎥 Tutoriais", callback_data='tutoriais')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "Escolha um treinamento:"

    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text=message_text, reply_markup=reply_markup)

async def handle_treinamento_callback(update: Update, context: CallbackContext):
    """Lida com os callbacks do menu de treinamento."""
    query = update.callback_query
    user_mention = f"@{query.from_user.username}" if query.from_user.username else query.from_user.first_name
    await query.answer()

    action = query.data.split('_')[0]

    if action in ['apoio', 'tutoriais']:
        buttons = [
            [InlineKeyboardButton(m['title'], callback_data=f"{action}_{i}")]
            for i, m in enumerate(TRAINING_MATERIALS.get(action, []))
        ]
        buttons.append([InlineKeyboardButton("⬅️ Voltar", callback_data='voltar')])
        await query.edit_message_text(f"{user_mention}, selecione o material:", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data.startswith(('apoio_', 'tutoriais_')):
        material_type, index_str = query.data.split('_')
        material = TRAINING_MATERIALS.get(material_type, [])[int(index_str)]
        await context.bot.send_document(chat_id=query.message.chat.id, document=material.get("file_id"))
        await context.bot.send_message(chat_id=query.message.chat.id, text=f"'{material.get('title')}' enviado. 📤")

    elif query.data == 'voltar':
        await treinamento(update=update, context=context)

