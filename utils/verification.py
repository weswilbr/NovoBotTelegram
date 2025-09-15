# NOME DO ARQUIVO: utils/verification.py
# REFACTOR: A verificação de membro de grupo foi desativada para remover a restrição.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

logger = logging.getLogger(__name__)

def group_member_required(func):
    """
    Decorator que originalmente restringia o acesso.
    Agora, permite o acesso a todos os utilizadores para desativar a restrição.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # A verificação foi removida, a função original é executada diretamente.
        return await func(update, context, *args, **kwargs)
    return wrapper

# As funções abaixo não são mais usadas pelo decorator, mas são mantidas
# caso queira reativar a funcionalidade no futuro.
async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    from config import CANAL_ID_2
    from telegram.constants import ChatMemberStatus
    from telegram.error import BadRequest

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