# NOME DO ARQUIVO: utils/verification.py
# REFACTOR: A verificação de membro de grupo foi completamente desativada para resolver erros de event loop.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

logger = logging.getLogger(__name__)

def group_member_required(func):
    """
    Decorator que originalmente restringia o acesso.
    Agora, permite o acesso a todos os utilizadores para desativar a restrição
    e evitar o erro 'Event loop is closed' no ambiente da Vercel.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # A verificação foi removida. A função original é chamada diretamente.
        return await func(update, context, *args, **kwargs)
    return wrapper