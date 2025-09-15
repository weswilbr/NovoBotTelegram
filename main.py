# main.py – versão enxuta com algumas melhorias de robustez
import logging
import sys
from pathlib import Path
from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters,
)

from config import BOT_TOKEN, CANAL_ID_2
from core.handlers import callback_router

# ------------------------------------------------------------------- #
# Logging
# ------------------------------------------------------------------- #
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    force=True,                     # garante formatação mesmo em PTB
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------- #
# Sanity-check do token
# ------------------------------------------------------------------- #
if not BOT_TOKEN:
    logger.critical("CRÍTICO: BOT_TOKEN não foi encontrado.")
    sys.exit(1)

# ------------------------------------------------------------------- #
# PTB Application
# ------------------------------------------------------------------- #
ptb_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# ------------------------------------------------------------------- #
# Imports de handlers (após PTB para evitar cold-start maior)
# ------------------------------------------------------------------- #
from features.admin.commands import (
    listar_admins, silenciar, banir, desbanir, fixar, desfixar,
    enviartextocanal,
)
from features.general.help_command import start, ajuda
from features.community.private_messaging import handle_private_message
from features.community.welcome import (
    darboasvindas_handler, welcome_callbacks_handler, handle_verification_callback,
    handle_unverified_text_message, CALLBACK_REGRAS, CALLBACK_INICIO, CALLBACK_MENU,
    VERIFY_MEMBER_CALLBACK,
)
from features.business.opportunity import apresentacaooportunidade
from features.business.brochures import folheteria
from features.business.glossary import glossario
from features.products.handlers import beneficiosprodutos
from features.business.marketing import marketing_rede
from features.business.rewards import recompensas
from features.business.transfer_factors import fatorestransferencia
from features.business.factory import fabrica4life
from features.general.bonus_builder import bonus_construtor
from features.community.rules import mostrar_regras
from features.community.invites import mostrar_convites
from features.creative.art_creator import artes
from features.training.training import treinamento
from features.business.ranking import mostrar_ranking
from features.community.channels import canais
from features.community.loyalty import fidelidade
from features.business.tables import tabelas_menu
from features.user_tools.store_finder import loja_handler

from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler

# ------------------------------------------------------------------- #
# Registro dos handlers
# ------------------------------------------------------------------- #
def register_handlers(app: Application) -> None:
    user_cmds = {
        "start": start, "ajuda": ajuda, "produtos": beneficiosprodutos,
        "apresentacaooportunidade": apresentacaooportunidade, "folheteria": folheteria,
        "glossario": glossario, "marketingrede": marketing_rede, "recompensas": recompensas,
        "fatorestransferencia": fatorestransferencia, "fabrica4life": fabrica4life,
        "bonusconstrutor": bonus_construtor, "regras": mostrar_regras,
        "convite": mostrar_convites, "artes": artes, "treinamento": treinamento,
        "ranking": mostrar_ranking, "canais": canais, "fidelidade": fidelidade,
        "tabelas": tabelas_menu,
    }
    for cmd, handler in user_cmds.items():
        app.add_handler(CommandHandler(cmd, handler))

    app.add_handler(loja_handler)       # já é Handler
    admin_cmds = {
        "listaradmins": listar_admins, "silenciar": silenciar, "banir": banir,
        "desbanir": desbanir, "fixar": fixar, "desfixar": desfixar,
        "enviartextocanal": enviartextocanal,
    }
    for cmd, handler in admin_cmds.items():
        app.add_handler(CommandHandler(cmd, handler))

    # Callbacks & mensagens
    app.add_handler(CallbackQueryHandler(
        welcome_callbacks_handler,
        pattern=f"^({CALLBACK_REGRAS}|{CALLBACK_INICIO}|{CALLBACK_MENU}|ajuda_.*)$",
    ))
    app.add_handler(CallbackQueryHandler(handle_verification_callback,
                                         pattern=f"^{VERIFY_MEMBER_CALLBACK}$"))
    app.add_handler(CallbackQueryHandler(callback_router))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                                   darboasvindas_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
                                   handle_private_message))
    if CANAL_ID_2:
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)),
            handle_unverified_text_message,
        ))

    # Utilitários
    app.add_handler(get_file_id_handler())
    app.add_handler(setup_group_id_handler())
    app.add_error_handler(error_handler)

register_handlers(ptb_app)

# ------------------------------------------------------------------- #
# FastAPI
# ------------------------------------------------------------------- #
app = FastAPI()

# favicon e outros estáticos (opcional)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.post("/")
async def webhook(request: Request, background_tasks: BackgroundTasks) -> Response:
    """Recebe update do Telegram e processa em background."""
    try:
        await ptb_app.initialize()      # idempotente
        update = Update.de_json(await request.json(), ptb_app.bot)
        background_tasks.add_task(ptb_app.process_update, update)
        return Response(status_code=200)
    except Exception as exc:
        logger.exception("Erro ao processar update")
        return Response(content=f"Erro interno: {exc}", status_code=500)

@app.get("/")
async def healthcheck():
    return {"status": "ok", "message": "Bot está rodando e pronto para receber webhooks"}