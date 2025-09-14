# NOME DO ARQUIVO: main.py
# REFACTOR: Versão final adaptada para deploy na Vercel via Webhooks.

import logging
import sys
import locale
import os
from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters
)

# --- Módulos de Configuração e Core ---
# BOT_TOKEN será pego das variáveis de ambiente da Vercel
from config import BOT_TOKEN, CANAL_ID_2
from core.handlers import callback_router

# --- Módulos de Funcionalidades (Features) ---
# (Todas as suas importações de 'features' e 'utils' permanecem aqui, sem alterações)
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

# --- Módulos de Utilitários (Utils) ---
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler
from utils.monitoring import commands as monitoring_commands
from utils.monitoring.tracker import UsageTracker

# --- Configuração do Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constantes para o Webhook ---
# A Vercel define a porta dinamicamente através de uma variável de ambiente.
PORT = int(os.environ.get('PORT', 8443))

def register_command_handlers(app: Application) -> None:
    # (Esta função permanece exatamente a mesma)
    # ... cole aqui a sua função register_command_handlers ...
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
    for command, handler in command_handlers.items():
        app.add_handler(CommandHandler(command, handler))
    app.add_handler(store_finder.loja_handler)


def register_callback_handlers(app: Application) -> None:
    # (Esta função permanece exatamente a mesma)
    # ... cole aqui a sua função register_callback_handlers ...
    app.add_handler(CallbackQueryHandler(welcome.welcome_callbacks_handler, pattern=f'^({welcome.CALLBACK_REGRAS}|{welcome.CALLBACK_INICIO}|{welcome.CALLBACK_MENU}|ajuda_.*)$'))
    app.add_handler(CallbackQueryHandler(welcome.handle_verification_callback, pattern=f'^{welcome.VERIFY_MEMBER_CALLBACK}$'))
    app.add_handler(CallbackQueryHandler(callback_router))


def register_message_handlers(app: Application) -> None:
    # (Esta função permanece exatamente a mesma)
    # ... cole aqui a sua função register_message_handlers ...
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.darboasvindas_handler))
    if CANAL_ID_2:
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)), welcome.handle_unverified_text_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, private_messaging.handle_private_message))


def register_utility_handlers(app: Application) -> None:
    # (Esta função permanece exatamente a mesma)
    # ... cole aqui a sua função register_utility_handlers ...
    app.add_handler(get_file_id_handler())
    app.add_handler(setup_group_id_handler())
    app.add_error_handler(error_handler)


# --- Aplicação Principal para Vercel ---
if not BOT_TOKEN:
    logger.critical("CRÍTICO: BOT_TOKEN não foi encontrado.")
    sys.exit(1)

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    logger.warning("Locale 'pt_BR.UTF-8' não suportado. Usando locale padrão.")

# Cria a aplicação
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Registra todos os handlers (isso não muda)
application.bot_data['usage_tracker'] = UsageTracker()
register_command_handlers(application)
register_callback_handlers(application)
register_message_handlers(application)
register_utility_handlers(application)

# A Vercel precisa de um endpoint HTTP para receber os webhooks
# A biblioteca python-telegram-bot lida com isso internamente
# Esta é a única parte que precisa estar no escopo global para a Vercel
async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Função que a Vercel irá chamar para cada update do Telegram."""
    await application.process_update(update)