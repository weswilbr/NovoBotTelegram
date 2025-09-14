# NOME DO ARQUIVO: main.py
# REFACTOR: Versão final otimizada para Vercel com Flask e asyncio.

import logging
import asyncio
import json
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, ContextTypes,
    CommandHandler, MessageHandler, CallbackQueryHandler, filters
)

# --- Módulos de Configuração e Core ---
from config import BOT_TOKEN, CANAL_ID_2
from core.handlers import callback_router

# --- Módulos de Funcionalidades e Utilitários ---
from features.admin import commands as admin_commands
from features.business import (
    opportunity, rewards, ranking, factory, transfer_factors,
    brochures, glossary, tables, marketing, planning
)
from features.community import (
    welcome, rules, invites, channels, loyalty, private_messaging
)
from features.creative import art_creator
from features.general import start, help, bonus_builder
from features.products import handlers as product_handlers
from features.training import training
from features.user_tools import store_finder
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler
from utils.monitoring import commands as monitoring_commands
from utils.monitoring.tracker import UsageTracker

# --- Configuração do Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Inicialização da Aplicação do Bot (Escopo Global) ---
# A aplicação é construída APENAS UMA VEZ quando a função serverless "acorda".
# Isso é muito mais eficiente do que reconstruí-la a cada mensagem.
if not BOT_TOKEN:
    raise ValueError("CRÍTICO: BOT_TOKEN não foi encontrado.")

ptb_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Registra todos os handlers
ptb_app.bot_data['usage_tracker'] = UsageTracker()

def register_command_handlers(app: Application) -> None:
    command_handlers = {
        "start": start.start, "ajuda": help.ajuda, "produtos": product_handlers.beneficiosprodutos,
        "bonusconstrutor": bonus_builder.bonus_construtor, "marketingrede": marketing.marketing_rede,
        "recompensas": rewards.mostrar_recompensas, "apresentacao": opportunity.apresentacaooportunidade,
        "fatorestransferencia": transfer_factors.fatorestransferencia, "fabrica4life": factory.fabrica4life,
        "folheteria": brochures.folheteria, "glossario": glossary.glossario,
        "tabelas": tables.tabelas_menu, "planificacao": planning.enviar_planificacao,
        "ranking": ranking.mostrar_ranking, "regras": rules.mostrar_regras,
        "convite": invites.mostrar_convites, "canais": channels.canais,
        "fidelidade": loyalty.fidelidade, "artes": art_creator.artes,
        "treinamento": training.treinamento, "listaradmins": admin_commands.listar_admins,
        "silenciar": admin_commands.silenciar, "banir": admin_commands.banir,
        "desbanir": admin_commands.desbanir, "fixar": admin_commands.fixar,
        "desfixar": admin_commands.desfixar, "enviartextocanal": admin_commands.enviartextocanal,
        "topusers": monitoring_commands.send_top_users_command, "resetusage": monitoring_commands.reset_usage_data_command,
    }
    for command, handler in command_handlers.items(): app.add_handler(CommandHandler(command, handler))
    app.add_handler(store_finder.loja_handler)

def register_callback_handlers(app: Application) -> None:
    app.add_handler(CallbackQueryHandler(welcome.welcome_callbacks_handler, pattern=f'^({welcome.CALLBACK_REGRAS}|{welcome.CALLBACK_INICIO}|{welcome.CALLBACK_MENU}|ajuda_.*)$'))
    app.add_handler(CallbackQueryHandler(welcome.handle_verification_callback, pattern=f'^{welcome.VERIFY_MEMBER_CALLBACK}$'))
    app.add_handler(CallbackQueryHandler(callback_router))

def register_message_handlers(app: Application) -> None:
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.darboasvindas_handler))
    if CANAL_ID_2:
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)), welcome.handle_unverified_text_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, private_messaging.handle_private_message))

def register_utility_handlers(app: Application) -> None:
    app.add_handler(get_file_id_handler())
    app.add_handler(setup_group_id_handler())
    app.add_error_handler(error_handler)

register_command_handlers(ptb_app)
register_callback_handlers(ptb_app)
register_message_handlers(ptb_app)
register_utility_handlers(ptb_app)

# Cria um loop de eventos asyncio que pode ser reutilizado entre as chamadas
loop = asyncio.get_event_loop()

# --- Servidor Flask para a Vercel ---
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook() -> tuple[str, int]:
    """Função que a Vercel chama. Ela recebe o update do Telegram e o processa."""
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, ptb_app.bot)
        
        # Executa a função assíncrona do bot no loop de eventos existente.
        # Isso é mais eficiente do que criar um novo loop para cada mensagem.
        loop.run_until_complete(ptb_app.process_update(update))
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Erro no webhook: {e}", exc_info=True)
        # Retorna uma tupla (resposta, código de status)
        return 'Internal Server Error', 500