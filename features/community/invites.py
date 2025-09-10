# NOME DO ARQUIVO: features/community/invites.py
# REFACTOR: Gerencia o comando /convite, exibindo e enviando modelos de convite.
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import CONVITES_TEXT
import logging

logger = logging.getLogger(__name__)

def get_invites_keyboard():
    """Cria o teclado com os modelos de convite."""
    keyboard = [
        [InlineKeyboardButton("📈 Profissional", callback_data="convite_1"), InlineKeyboardButton("😊 Amigável", callback_data="convite_2")],
        [InlineKeyboardButton("🌍 Flexível", callback_data="convite_3"), InlineKeyboardButton("💵 Renda Extra", callback_data="convite_4")],
        [InlineKeyboardButton("🎁 Oportunidade", callback_data="convite_14"), InlineKeyboardButton("💡 Solução", callback_data="convite_15")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def mostrar_convites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o menu de seleção de convites, tratando diferentes tipos de update."""
    reply_markup = get_invites_keyboard()
    text = "Escolha um modelo de convite:"
    
    chat_id = update.effective_chat.id if update.effective_chat else None

    if not chat_id:
        logger.error("Não foi possível determinar o chat_id em mostrar_convites.")
        return

    if update.callback_query and update.callback_query.message:
        try:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Erro ao editar mensagem em mostrar_convites: {e}. Enviando nova mensagem.")
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        logger.warning("mostrar_convites foi chamado sem um update comum, enviando mensagem para effective_chat.")
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


async def enviar_convite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia o texto do convite selecionado, com verificação de segurança."""
    query = update.callback_query
    
    if not query or not query.data:
        logger.warning("enviar_convite chamado sem uma callback query válida.")
        return

    chat_id = update.effective_chat.id if update.effective_chat else None
    if not chat_id:
        logger.error(f"Não foi possível determinar o chat_id para enviar o convite: {query.data}")
        await query.answer("Erro: Não foi possível determinar para onde enviar a mensagem.", show_alert=True)
        return

    convite_key = query.data
    texto_convite = CONVITES_TEXT.get(convite_key, "Modelo de convite não encontrado.")
    keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="voltar_convites")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query.message:
        try:
            await query.edit_message_text(texto_convite, reply_markup=reply_markup)
        except Exception as e:
            logger.error(f"Erro ao editar a mensagem com o convite: {e}. Enviando nova mensagem.")
            await context.bot.send_message(chat_id=chat_id, text=texto_convite, reply_markup=reply_markup)
    else:
        logger.warning(f"Não foi possível editar a mensagem para enviar o convite '{convite_key}'. Enviando nova mensagem.")
        await context.bot.send_message(chat_id=chat_id, text=texto_convite, reply_markup=reply_markup)

