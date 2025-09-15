# NOME DO ARQUIVO: utils/anti_flood.py
# VERSÃO: antiflood desativado – todas as chamadas passam direto.

import logging
from functools import wraps
from typing import Any, Awaitable, Callable

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)
logger.info("[anti_flood] Módulo carregado em modo OFF – nenhum bloqueio será aplicado.")

# --------------------------------------------------------------------------- #
# Decorator para comandos (/start, /produtos, etc.)
# --------------------------------------------------------------------------- #
def command_rate_limit(arg: Any = None, *, seconds: int = 0) -> Callable:  # type: ignore
    """
    Versão 'no-op'. Aceita ser usada com ou sem parênteses:
        @command_rate_limit
        @command_rate_limit()
        @command_rate_limit(5)
    Em todos os casos apenas devolve a função original.
    """
    if callable(arg):
        return arg  # usado como @command_rate_limit
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        return func
    return decorator

# --------------------------------------------------------------------------- #
# Função de verificação para cliques
# --------------------------------------------------------------------------- #
async def check_flood(update: Update, seconds: int = 0) -> bool:  # pylint: disable=unused-argument
    """
    Sempre retorna True, permitindo a continuidade do handler.
    Mantém a assinatura original para evitar refatorações.
    """
    return True