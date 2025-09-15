# NOME DO ARQUIVO: main.py
# --- Importações Padrão e de Terceiros ---
import logging
import sys
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters
)

# --- Configuração e Módulos do Bot ---
from config import BOT_TOKEN, CANAL_ID_2
from core.handlers import callback_router

# --- Handlers ---
from features.admin.commands import (
    listar_admins, silenciar, banir, desbanir, fixar, desfixar, enviartextocanal
)
from features.general.help_command import start, ajuda
from features.community.private_messaging import handle_private_message
from features.community.welcome import (
    darboasvindas_handler, welcome_callbacks_handler, handle_verification_callback,
    handle_unverified_text_message, CALLBACK_REGRAS, CALLBACK_INICIO, CALLBACK_MENU,
    VERIFY_MEMBER_CALLBACK
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

# --- Utilitários ---
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Validação Inicial ---
if not BOT_TOKEN:
    logger.critical("CRÍTICO: BOT_TOKEN não foi encontrado.")
    sys.exit(1)

# --- Construtor do Bot ---
ptb_app = ApplicationBuilder().token(BOT_TOKEN).build()

# --- Registro dos Handlers ---
# 1. Comandos de usuário
command_handlers = {
    "start": start, "ajuda": ajuda, "produtos": beneficiosprodutos,
    "apresentacaooportunidade": apresentacaooportunidade, "folheteria": folheteria,
    "glossario": glossario, "marketingrede": marketing_rede, "recompensas": recompensas,
    "fatorestransferencia": fatorestransferencia, "fabrica4life": fabrica4life,
    "bonusconstrutor": bonus_construtor, "regras": mostrar_regras, "convite": mostrar_convites,
    "artes": artes, "treinamento": treinamento, "ranking": mostrar_ranking,
    "canais": canais, "fidelidade": fidelidade, "tabelas": tabelas_menu
}
for command, handler in command_handlers.items():
    # Decorador de rastreamento removido
    ptb_app.add_handler(CommandHandler(command, handler))

# Adiciona o ConversationHandler para /minhaloja
ptb_app.add_handler(loja_handler)

# 2. Comandos de admin
admin_command_handlers = {
    # Comandos do tracker removidos
    "listaradmins": listar_admins, "silenciar": silenciar, "banir": banir,
    "desbanir": desbanir, "fixar": fixar, "desfixar": desfixar,
    "enviartextocanal": enviartextocanal
}
for command, handler in admin_command_handlers.items():
    ptb_app.add_handler(CommandHandler(command, handler))

# 3. Callbacks e mensagens
ptb_app.add_handler(CallbackQueryHandler(
    welcome_callbacks_handler,
    pattern=f"^({CALLBACK_REGRAS}|{CALLBACK_INICIO}|{CALLBACK_MENU}|ajuda_.*)$"
))
ptb_app.add_handler(CallbackQueryHandler(handle_verification_callback, pattern=f"^{VERIFY_MEMBER_CALLBACK}$"))
ptb_app.add_handler(CallbackQueryHandler(callback_router))
ptb_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, darboasvindas_handler))
ptb_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, handle_private_message))
if CANAL_ID_2:
    ptb_app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)),
        handle_unverified_text_message
    ))

# 4. Utilitários
ptb_app.add_handler(get_file_id_handler())
ptb_app.add_handler(setup_group_id_handler())
ptb_app.add_error_handler(error_handler)

# --- FastAPI App ---
app = FastAPI()

@app.post("/")
async def webhook(request: Request) -> Response:
    """Recebe update do Telegram via webhook."""
    try:
        if not ptb_app._initialized:
            await ptb_app.initialize()
        data = await request.json()
        update = Update.de_json(data, ptb_app.bot)
        await ptb_app.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        logger.exception("Erro ao processar update do Telegram")
        return Response(content=f"Erro interno: {e}", status_code=500)

@app.get("/")
async def healthcheck():
    """Healthcheck endpoint."""
    return {"status": "ok", "message": "Bot está rodando e pronto para receber webhooks"}