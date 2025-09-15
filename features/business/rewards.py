# features/business/rewards.py  (versão resiliente)
import logging
from io import BytesIO
from pathlib import Path

import httpx
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from features.products.data import MEDIA_GERAL

logger = logging.getLogger(__name__)

async def recompensas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    entry = MEDIA_GERAL.get("recompensas2024", {})
    doc_ref = entry.get("documento")

    if not doc_ref:
        await update.message.reply_text("⚠️ Documento de recompensas não encontrado.")
        return

    try:
        # Caso 1 ─ file_id (começa com AgAD ou CAAC etc.)
        if len(doc_ref) > 50 and not doc_ref.startswith(("http://", "https://", "/")):
            await context.bot.send_document(update.effective_chat.id, doc_ref)

        # Caso 2 ─ caminho local
        elif doc_ref.startswith(("/", "./")):
            path = Path(doc_ref).expanduser()
            if not path.exists():
                raise FileNotFoundError(path)
            with path.open("rb") as f:
                await context.bot.send_document(update.effective_chat.id, f)

        # Caso 3 ─ URL
        else:
            async with httpx.AsyncClient() as client:
                resp = await client.get(doc_ref, timeout=15)
            resp.raise_for_status()
            buf = BytesIO(resp.content)
            buf.name = Path(doc_ref).name or "recompensas.pdf"
            await context.bot.send_document(update.effective_chat.id, buf)

    except (TelegramError, httpx.HTTPError, FileNotFoundError, RuntimeError) as e:
        logger.error("Erro ao enviar o documento de recompensas: %s", e)
        await update.message.reply_text("⚠️ Não foi possível enviar o documento agora. Tente mais tarde.")