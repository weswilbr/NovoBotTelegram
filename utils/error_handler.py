# NOME DO ARQUIVO: utils/error_handler.py
# Handler global de exceções (python-telegram-bot v20+).

import logging
import traceback
import html
import json
from typing import Any

from telegram import Update
from telegram.error import BadRequest, Forbidden, TimedOut, NetworkError
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Lista de mensagens/erros que não merecem alertar o usuário
IGNORED_BADREQUESTS = (
    "message is not modified",
    "query is too old",
    "message to edit not found",
    "button_url_invalid",
)
# --------------------------------------------------------------------------- #

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Captura erros gerados por handlers, loga e (se necessário) avisa o usuário."""
    err: Exception = context.error  # tipo para autocomplete

    # 1) LOG DETALHADO (console ou CloudWatch)
    logger.error("Exceção ao processar update:", exc_info=err)

    # opcional: salvar trace resumido para debug local
    trace = "".join(traceback.format_exception(None, err, err.__traceback__))
    update_json = _stringify_update(update)
    logger.debug("TRACE:\n%s\nUPDATE:\n%s", trace, update_json)

    # 2) FILTRO – erros que NÃO devem ser mostrados ao usuário
    if (
        isinstance(err, BadRequest)
        and any(msg in str(err).lower() for msg in IGNORED_BADREQUESTS)
    ):
        return  # silencia completamente

    if isinstance(err, (TimedOut, NetworkError, Forbidden)):
        # rede instável ou bot foi bloqueado → silencia
        return

    # 3) NOTIFICAÇÃO ao usuário (apenas chats privados por padrão)
    if isinstance(update, Update) and update.effective_chat:
        chat = update.effective_chat
        if chat.type == "private":     # comente esta linha se quiser avisar grupos
            try:
                await context.bot.send_message(
                    chat_id=chat.id,
                    text="⚠️ Oops! Ocorreu um erro inesperado. Nossa equipe já foi notificada."
                )
            except Exception as e:     # noqa: BLE001
                logger.warning("Falha ao enviar aviso de erro ao usuário: %s", e)


# --------------------------------------------------------------------------- #
# Helper para exibir o update em JSON de forma legível
def _stringify_update(update: Any) -> str:
    if isinstance(update, Update):
        try:
            return json.dumps(update.to_dict(), indent=2, ensure_ascii=False)
        except Exception:  # noqa: BLE001
            return str(update)
    return str(update)