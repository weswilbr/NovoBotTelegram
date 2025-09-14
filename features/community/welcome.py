# NOME DO ARQUIVO: features/community/welcome.py
# REFACTOR: Gerencia o fluxo de boas-vindas e verificação de novos membros.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from telegram.constants import ParseMode

import config
from features.general.help import ajuda
from features.community.rules import mostrar_regras

logger = logging.getLogger(__name__)

# --- Constantes ---
# Usar constantes para callback_data e chaves de dicionário evita erros de digitação.
CALLBACK_REGRAS = "welcome_regras"
CALLBACK_INICIO = "welcome_inicio"
CALLBACK_MENU = "welcome_menu"
VERIFY_MEMBER_CALLBACK = "verify_member"

UNVERIFIED_MEMBERS_KEY = 'unverified_members'
WELCOME_MESSAGE_IDS_KEY = 'welcome_message_ids'

# --- Funções Auxiliares de Teclado ---
def _create_verification_keyboard() -> InlineKeyboardMarkup:
    """Cria o botão de verificação inicial."""
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Sou da Equipe de Triunfo", callback_data=VERIFY_MEMBER_CALLBACK)]])

def _create_rules_keyboard() -> InlineKeyboardMarkup:
    """Cria o botão para o usuário ler as regras."""
    return InlineKeyboardMarkup([[InlineKeyboardButton("📜 Ler as Regras do Grupo", callback_data=CALLBACK_REGRAS)]])

def _create_start_keyboard() -> InlineKeyboardMarkup:
    """Cria o botão para prosseguir após ler as regras."""
    return InlineKeyboardMarkup([[InlineKeyboardButton("▶️ Entendido, ir para o Início", callback_data=CALLBACK_INICIO)]])

def _create_menu_keyboard() -> InlineKeyboardMarkup:
    """Cria o botão para acessar o menu principal de comandos."""
    return InlineKeyboardMarkup([[InlineKeyboardButton("📋 Acessar o MENU de Comandos", callback_data=CALLBACK_MENU)]])

# --- Handlers Principais ---

async def darboasvindas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Envia mensagem de boas-vindas e inicia o fluxo de verificação para novos membros.
    Esta função é acionada sempre que um ou mais novos membros entram no chat.
    """
    if not (update.message and update.message.new_chat_members and context.chat_data is not None):
        return

    chat_id = update.message.chat_id
    if chat_id != config.CANAL_ID_2:
        return

    # 'setdefault' garante que as chaves existam em chat_data, evitando KeyErrors.
    context.chat_data.setdefault(UNVERIFIED_MEMBERS_KEY, [])
    context.chat_data.setdefault(WELCOME_MESSAGE_IDS_KEY, {})

    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        user_id = member.id
        nome_usuario = member.first_name.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')

        # Adiciona o usuário à lista de não verificados.
        if user_id not in context.chat_data[UNVERIFIED_MEMBERS_KEY]:
            context.chat_data[UNVERIFIED_MEMBERS_KEY].append(user_id)

        mensagem_boas_vindas = (
            f"🎉 Bem\\-vindo\\(a\\) ao grupo, *{nome_usuario}*\\! 🎉\n\n"
            "Este é um espaço exclusivo para membros da *Equipe de Triunfo*\\.\n\n"
            "Para garantir a segurança e a qualidade do nosso grupo, por favor, "
            "*verifique sua participação* clicando no botão abaixo\\."
        )
        
        try:
            sent_message = await context.bot.send_message(
                chat_id=chat_id,
                text=mensagem_boas_vindas,
                reply_markup=_create_verification_keyboard(),
                parse_mode=ParseMode.MARKDOWN_V2
            )
            # Armazena o ID da mensagem para que possamos deletá-la após a verificação.
            context.chat_data[WELCOME_MESSAGE_IDS_KEY][user_id] = sent_message.message_id
        except TelegramError as e:
            logger.error(f"Erro ao enviar mensagem de boas-vindas para {user_id}: {e}", exc_info=True)

async def handle_verification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processa o clique no botão de verificação."""
    query = update.callback_query
    if not (query and query.message and query.from_user and context.chat_data is not None):
        if query: await query.answer("Ocorreu um erro. Tente novamente.", show_alert=True)
        return

    user_id_clicked = query.from_user.id
    chat_id = query.message.chat_id
    unverified_list = context.chat_data.get(UNVERIFIED_MEMBERS_KEY, [])

    if user_id_clicked in unverified_list:
        await query.answer("Verificação bem-sucedida!")
        
        # Remove o usuário da lista de não verificados.
        unverified_list.remove(user_id_clicked)
        
        # Remove a mensagem de verificação original para manter o chat limpo.
        welcome_messages = context.chat_data.get(WELCOME_MESSAGE_IDS_KEY, {})
        message_id = welcome_messages.pop(user_id_clicked, None)
        if message_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except TelegramError as e:
                logger.warning(f"Falha ao deletar mensagem de boas-vindas {message_id}: {e}")

        nome_usuario = query.from_user.first_name.replace('_', '\\_').replace('*', '\\*')
        success_message = f"✅ *{nome_usuario}* agora tem acesso total ao grupo\\! Seja muito bem\\-vindo\\(a\\) à Equipe de Triunfo\\."
        await context.bot.send_message(chat_id=chat_id, text=success_message, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=_create_rules_keyboard())
    else:
        await query.answer("Você já está verificado(a)!", show_alert=True)
        # Deleta a mensagem de verificação antiga se o usuário já verificado clicar nela.
        try:
            await query.message.delete()
        except TelegramError:
            pass # A mensagem pode já ter sido deletada.

async def welcome_callbacks_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com os callbacks do fluxo pós-verificação (Regras, Início, Menu)."""
    query = update.callback_query
    if not query or not query.message:
        return
        
    await query.answer()
    data = query.data

    if data == CALLBACK_REGRAS:
        # Chama a função de regras e, se for bem-sucedida, atualiza o botão.
        if await mostrar_regras(update, context, edit_message=True):
            await query.edit_message_reply_markup(reply_markup=_create_start_keyboard())
    
    elif data == CALLBACK_INICIO:
        mensagem_inicio = "✅ Ótimo\\! Agora que você conhece as regras, pode explorar tudo que o nosso bot oferece\\.\n\nClique no botão *MENU* abaixo para ver a lista completa de comandos e materiais disponíveis\\."
        await query.edit_message_text(text=mensagem_inicio, reply_markup=_create_menu_keyboard(), parse_mode=ParseMode.MARKDOWN_V2)

    elif data == CALLBACK_MENU:
        # Remove o botão "MENU" e envia a mensagem de ajuda.
        await query.edit_message_reply_markup(reply_markup=None)
        await ajuda(update, context)

async def handle_unverified_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Detecta e silencia usuários não verificados que tentam enviar mensagens.
    CORREÇÃO: Esta função agora usa a chamada direta da API para restringir membros.
    """
    if not (update.message and update.message.text and update.effective_user and context.chat_data is not None):
        return

    user = update.effective_user
    chat = update.effective_chat
    if not chat or chat.id != config.CANAL_ID_2:
        return

    if user.id in context.chat_data.get(UNVERIFIED_MEMBERS_KEY, []):
        logger.info(f"Usuário não verificado {user.id} ({user.first_name}) enviou texto. Removendo mensagem e restringindo.")
        
        permissions = ChatPermissions(can_send_messages=False)
        try:
            # Silencia o usuário indefinidamente (até que ele se verifique).
            await context.bot.restrict_chat_member(chat_id=chat.id, user_id=user.id, permissions=permissions)
            
            # Deleta a mensagem infratora.
            await update.message.delete()
            
            nome_usuario = user.first_name.replace('_', '\\_').replace('*', '\\*')
            silence_notice = (f"⚠️ *{nome_usuario}*, você precisa se verificar para poder interagir no grupo\\.\n\n"
                              "Por favor, encontre sua mensagem de boas\\-vindas e clique no botão de verificação\\.")
            await context.bot.send_message(chat_id=chat.id, text=silence_notice, parse_mode=ParseMode.MARKDOWN_V2)
            
        except TelegramError as e:
            logger.error(f"Falha ao restringir ou deletar mensagem do usuário {user.id}: {e}")