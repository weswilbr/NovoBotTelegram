# NOME DO ARQUIVO: utils/verification.py
# REFACTOR: Adicionado um bypass para administradores na verificação de membro.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatMemberStatus
from telegram.error import BadRequest
from functools import wraps
# Importa as variáveis de configuração
from config import CANAL_ID_2, ADMIN_USER_IDS

logger = logging.getLogger(__name__)

RESTRICTION_MSG = "🛡️ *Acesso Restrito*\n\nPara usar esta função, você precisa ser um membro ativo do nosso grupo de suporte."

async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Verifica se um utilizador é membro do grupo alvo."""
    if not CANAL_ID_2:
        logger.error("CANAL_ID_2 não está definido na configuração para verificação.")
        return False
    try:
        chat_member = await context.bot.get_chat_member(chat_id=CANAL_ID_2, user_id=user_id)
        return chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except BadRequest:
        logger.info(f"Utilizador {user_id} não encontrado no grupo {CANAL_ID_2}.")
        return False
    except Exception as e:
        logger.error(f"Erro ao verificar membro {user_id} no grupo {CANAL_ID_2}: {e}")
        return False

def group_member_required(func):
    """Decorator que restringe o acesso, mas permite que admins (donos) o ignorem."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user: return

        # Se o ID do utilizador estiver na lista de admins, permite o acesso imediatamente.
        if user.id in ADMIN_USER_IDS:
            return await func(update, context, *args, **kwargs)

        # Para os outros utilizadores, faz a verificação normal.
        if await is_user_member(user.id, context):
            return await func(update, context, *args, **kwargs)
        else:
            logger.warning(f"Acesso negado para o utilizador {user.id} (não membro) ao handler {func.__name__}.")
            target_chat = update.callback_query.message.chat if update.callback_query and update.callback_query.message else (update.message.chat if update.message else None)
            if target_chat:
                await context.bot.send_message(
                    chat_id=target_chat.id,
                    text=RESTRICTION_MSG,
                    parse_mode=ParseMode.MARKDOWN
                )
    return wrapper