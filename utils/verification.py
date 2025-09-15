# NOME DO ARQUIVO: utils/verification.py
# REFACTOR: A verificação de membro foi desativada para corrigir o erro e remover a restrição.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

logger = logging.getLogger(__name__)

def group_member_required(func):
    """
    Decorator de substituição. Executa a função do comando diretamente,
    ignorando qualquer verificação de membro de grupo para evitar erros no servidor.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # A verificação foi removida, a função original é executada diretamente.
        return await func(update, context, *args, **kwargs)
    return wrapper