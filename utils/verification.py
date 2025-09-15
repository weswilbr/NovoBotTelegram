# NOME DO ARQUIVO: utils/verification.py
# VERSÃO DESATIVADA: Permite o acesso a todos os comandos sem restrição.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

logger = logging.getLogger(__name__)

def group_member_required(func):
    """
    Decorator de substituição. Executa a função do comando diretamente,
    ignorando qualquer verificação de membro de grupo.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # A verificação foi removida, a função original é executada diretamente.
        return await func(update, context, *args, **kwargs)
    return wrapper