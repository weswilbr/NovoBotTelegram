# utils/anti_flood.py
"""Decorators e helpers para limitar spam de comandos/callbacks."""

import time
import logging
from functools import wraps
from typing import Callable, Awaitable, Any, Dict

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --------------------------------------------------------------------------- #
# Estruturas em memória
# --------------------------------------------------------------------------- #
_user_last_cmd: Dict[int, float] = {}
_user_last_click: Dict[int, float] = {}

DEFAULT_CMD_LIMIT = 3     # segundos
DEFAULT_CLICK_LIMIT = 2   # segundos


# --------------------------------------------------------------------------- #
# Decorator para comandos (/start, /produtos, etc.)
# Funciona com ou sem parênteses:
#   @command_rate_limit
#   @command_rate_limit()
#   @command_rate_limit(5)
# --------------------------------------------------------------------------- #
def command_rate_limit(
    arg: Any = None, *, seconds: int = DEFAULT_CMD_LIMIT
) -> Callable:                                         # type: ignore
    """
    Decorator antiflood para comandos de texto.
    Uso:
        @command_rate_limit              # 3s
        @command_rate_limit()            # 3s (idem)
        @command_rate_limit(5)           # 5s
        @command_rate_limit(seconds=10)  # 10s
    """
    # Caso seja usado sem (), o primeiro argumento é a função decorada
    if callable(arg) and not isinstance(arg, (int, float)):
        func = arg
        return _wrap_command(func, seconds)

    # Caso contrário, devolvemos um decorator esperando a função
    def real_decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        return _wrap_command(func, seconds)

    return real_decorator


def _wrap_command(func: Callable[..., Awaitable[Any]], seconds: int):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user:
            return

        uid = update.effective_user.id
        now = time.monotonic()
        last = _user_last_cmd.get(uid, 0)

        if now - last < seconds:
            logger.info("[anti_flood] comando de %s bloqueado (%ss)", uid, seconds)
            return

        _user_last_cmd[uid] = now
        return await func(update, context, *args, **kwargs)

    return wrapper


# --------------------------------------------------------------------------- #
# Função para callbacks (botões)
# --------------------------------------------------------------------------- #
async def check_flood(update: Update, seconds: int = DEFAULT_CLICK_LIMIT) -> bool:
    """
    Retorna False se o usuário clicou muito rápido.
    Use no callback_router:

        if not await check_flood(update):
            return
    """
    query = update.callback_query
    if not (query and update.effective_user):
        return False

    uid = update.effective_user.id
    now = time.monotonic()
    last = _user_last_click.get(uid, 0)

    if now - last < seconds:
        remaining = int(seconds - (now - last))
        try:
            await query.answer(f"⌛ Aguarde {remaining}s.", show_alert=True)
        except TelegramError as e:
            logger.info("[anti_flood] falha ao enviar alerta: %s", e)
        return False

    _user_last_click[uid] = now
    return True