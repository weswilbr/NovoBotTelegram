# NOME DO ARQUIVO: features/admin/commands.py
# REFACTOR: Gerencia todos os comandos e a lógica de verificação para administradores.

import logging
from telegram import ChatMember, ChatPermissions, Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest, TelegramError
from telegram.constants import ParseMode, ChatMemberStatus

from config import ADMIN_USER_IDS, CANAL_ID_2
from functools import wraps

logger = logging.getLogger(__name__)

async def is_admin_in_group(user_id: int, chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Verifica se um usuário é admin ou dono de um chat específico."""
    if not chat_id:
        logger.error("is_admin_in_group chamado sem chat_id.")
        return False
    try:
        chat_member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except (BadRequest, TelegramError) as e:
        logger.warning(f"Erro ao verificar status de admin para user {user_id} no chat {chat_id}: {e}")
        return False

def admin_required(func):
    """Decorator para restringir comandos a administradores do grupo principal."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user: return

        if await is_admin_in_group(user.id, CANAL_ID_2, context):
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("Apenas administradores podem usar este comando.")
    return wrapper

# Funções de admin (silenciar, banir, etc.) continuam aqui...
async def listar_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

@admin_required
async def silenciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

@admin_required
async def banir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

@admin_required
async def desbanir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

@admin_required
async def fixar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

@admin_required
async def desfixar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

@admin_required
async def enviartextocanal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Implementação...
    pass

async def _silence_user_core(chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE, duration_seconds: int = 0) -> bool:
    """Função central para silenciar um usuário."""
    try:
        permissions = ChatPermissions(
            can_send_messages=False, can_send_media_messages=False,
            can_send_polls=False, can_send_other_messages=False,
            can_add_web_page_previews=False, can_change_info=False,
            can_invite_users=False, can_pin_messages=False
        )
        await context.bot.restrict_chat_member(
            chat_id=chat_id, user_id=user_id, permissions=permissions
        )
        return True
    except Exception as e:
        logger.error(f"Falha ao silenciar usuário {user_id} no chat {chat_id}: {e}")
        return False

