# NOME DO ARQUIVO: features/business/kits.py
# REFACTOR: Handler para o comando /seguimento, enviando kits de produtos e negócios.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from features.products.data import MEDIA

logger = logging.getLogger(__name__)

async def seguimento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu para escolher o kit de seguimento."""
    keyboard = [
        [InlineKeyboardButton("📦 Kit Produtos", callback_data='kit_produtos')],
        [InlineKeyboardButton("💼 Kit Negócio", callback_data='kit_negocios')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Escolha o kit que deseja receber:",
        reply_markup=reply_markup
    )

async def handle_kit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o kit selecionado para o privado do usuário."""
    query = update.callback_query
    user_id = update.effective_user.id
    original_chat_id = query.message.chat.id

    kit_type = query.data # 'kit_produtos' or 'kit_negocios'
    
    # Esta parte é um exemplo e precisa dos file_ids corretos em data.py
    # para funcionar.
    if kit_type == 'kit_produtos':
        await context.bot.send_message(
            chat_id=original_chat_id,
            text="📦 *Kit Produtos* enviado para o seu privado!",
            parse_mode='Markdown'
        )
    elif kit_type == 'kit_negocios':
        await context.bot.send_message(
            chat_id=original_chat_id,
            text="💼 *Kit Negócio* enviado para o seu privado!",
            parse_mode='Markdown'
        )