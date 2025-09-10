# NOME DO ARQUIVO: features/community/welcome.py
# REFACTOR: Gerencia o fluxo de boas-vindas e verificação de novos membros.
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from telegram.constants import ParseMode, ChatMemberStatus
import config

# Importação corrigida com o caminho completo do módulo
from features.admin.commands import _silence_user_core
from features.general.help import ajuda
from features.community.rules import mostrar_regras

logger = logging.getLogger(__name__)

# Constantes para callbacks
CALLBACK_REGRAS = "welcome_regras"
CALLBACK_INICIO = "welcome_inicio"
CALLBACK_MENU = "welcome_menu"
VERIFY_MEMBER_CALLBACK = "verify_member"

# Chaves para o chat_data
UNVERIFIED_MEMBERS_KEY = 'unverified_members'
WELCOME_MESSAGE_IDS_KEY = 'welcome_message_ids'

# --- Funções Auxiliares de Teclado ---
def criar_teclado_regras() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("📜 Regras do Grupo", callback_data=CALLBACK_REGRAS)]])

def criar_teclado_inicio() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("▶️ INICIO", callback_data=CALLBACK_INICIO)]])

def criar_teclado_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("📋 MENU", callback_data=CALLBACK_MENU)]])

def criar_teclado_verificacao() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Sou da Equipe de Triunfo", callback_data=VERIFY_MEMBER_CALLBACK)]])

# --- Handlers Principais ---

async def darboasvindas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia mensagem de boas-vindas e inicia o fluxo de verificação para novos membros."""
    if not (update.message and update.message.new_chat_members and context.chat_data is not None):
        return

    chat_id = update.message.chat_id
    if str(chat_id) != str(config.CANAL_ID_2):
        return

    # Inicializa os dicionários de forma segura
    context.chat_data.setdefault(UNVERIFIED_MEMBERS_KEY, [])
    context.chat_data.setdefault(WELCOME_MESSAGE_IDS_KEY, {})

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        user_id = member.id
        nome_usuario = member.first_name

        if user_id not in context.chat_data[UNVERIFIED_MEMBERS_KEY]:
            context.chat_data[UNVERIFIED_MEMBERS_KEY].append(user_id)

        mensagem_boas_vindas = (
            f"🎉 Bem\\-vindo\\(a\\) ao grupo, \\*{nome_usuario}\\*\\! 🎉\n\n"
            "Este grupo é para membros da \\*Equipe de Triunfo\\*\\.\n\n"
            "Para ter acesso completo, por favor, \\*verifique sua participação\\* clicando no botão abaixo\\."
        )
        
        try:
            sent_message = await context.bot.send_message(
                chat_id=chat_id,
                text=mensagem_boas_vindas,
                reply_markup=criar_teclado_verificacao(),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            context.chat_data[WELCOME_MESSAGE_IDS_KEY][user_id] = sent_message.message_id
        except Exception as e:
            logger.error(f"Erro ao enviar msg de boas-vindas para {user_id}: {e}", exc_info=True)

async def welcome_callbacks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks dos botões de boas-vindas (Regras, Início, Menu)."""
    query = update.callback_query
    if not (query and query.message):
        if query: await query.answer("Erro: Mensagem original não encontrada.")
        return
        
    await query.answer()

    if query.data == CALLBACK_REGRAS:
        if await mostrar_regras(update, context, edit_message=True):
            await query.edit_message_reply_markup(reply_markup=criar_teclado_inicio())
    
    elif query.data == CALLBACK_INICIO:
        mensagem_inicio = "✅ Obrigado por ler as regras\\!\n\nUse o botão \\*MENU\\* para ver as opções\\."
        await query.edit_message_text(text=mensagem_inicio, parse_mode=ParseMode.MARKDOWN_V2)
        await query.message.reply_text("👇 Clique para acessar o menu:", reply_markup=criar_teclado_menu())

    elif query.data == CALLBACK_MENU:
        await ajuda(update, context)
        await query.edit_message_reply_markup(reply_markup=None)

async def handle_verification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processa o clique no botão de verificação."""
    query = update.callback_query
    if not (query and query.message and query.from_user and context.chat_data is not None):
        if query: await query.answer("Erro interno.")
        return

    await query.answer("Verificando...")
    user_id = query.from_user.id
    chat_id = query.message.chat_id

    unverified_list = context.chat_data.get(UNVERIFIED_MEMBERS_KEY, [])
    if user_id in unverified_list:
        unverified_list.remove(user_id)
        
        welcome_messages = context.chat_data.get(WELCOME_MESSAGE_IDS_KEY, {})
        message_id = welcome_messages.pop(user_id, None)
        if message_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                logger.warning(f"Falha ao deletar msg de boas-vindas {message_id}: {e}")

        success_message = f"✅ \\*{query.from_user.first_name}\\* verificou sua participação\\! Bem\\-vindo\\(a\\) ao grupo\\."
        await context.bot.send_message(chat_id=chat_id, text=success_message, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.answer("Você já está verificado ou esta mensagem é antiga.", show_alert=True)

async def handle_unverified_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Silencia usuários não verificados que enviam mensagens de texto."""
    if not (update.message and update.message.text and update.effective_user and context.chat_data is not None):
        return

    user = update.effective_user
    chat = update.effective_chat
    if not chat or str(chat.id) != str(config.CANAL_ID_2):
        return

    unverified_list = context.chat_data.get(UNVERIFIED_MEMBERS_KEY, [])
    if user.id in unverified_list:
        logger.warning(f"Usuário não verificado {user.id} enviou texto. Silenciando.")
        if await _silence_user_core(chat.id, user.id, context, duration_seconds=0):
            try:
                await update.message.delete()
            except Exception as e:
                logger.warning(f"Falha ao deletar msg de usuário não verificado: {e}")
            
            silence_notice = (f"⚠️ \\*{user.first_name}\\*, você foi silenciado\\(a\\)\\.\n"
                              "Clique no botão na sua mensagem de boas\\-vindas para poder interagir\\.")
            await context.bot.send_message(chat_id=chat.id, text=silence_notice, parse_mode=ParseMode.MARKDOWN_V2)

