# NOME DO ARQUIVO: main.py
# REFACTOR: Ponto de entrada principal da aplicação. Orquestra a inicialização e o registro de todos os handlers.

import logging
import locale
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
)

# --- Módulos de Configuração e Core ---
from config import BOT_TOKEN, CANAL_ID_2
from core.handlers import callback_router

# --- Módulos de Funcionalidades (Features) ---
from features.admin.commands import (
    listar_admins, silenciar, banir, desbanir, fixar, desfixar, enviartextocanal
)
from features.business import (
    opportunity, rewards, ranking, factory, transfer_factors,
    brochures, glossary, tables, marketing, planning, kits
)
from features.community import (
    welcome, rules, invites, channels, loyalty, private_messaging
)
from features.creative import art_creator
from features.general import start, help, bonus_builder
from features.products import handlers as product_handlers
from features.training import training, reading_guide
from features.user_tools import store_finder

# --- Módulos de Utilitários (Utils) ---
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler
from utils.monitoring.commands import send_top_users_command, reset_usage_data_command
from utils.monitoring.motivation import enviar_motivacao_agendada
from utils.monitoring.tracker import UsageTracker

# --- Configuração do Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def register_command_handlers(application: Application) -> None:
    """Registra todos os manipuladores de comando e de conversa."""
    
    application.add_handler(store_finder.loja_handler)

    # Handlers de Comando Simples
    command_handlers = {
        "start": start.start,
        "ajuda": help.ajuda,
        "admin_listar": listar_admins, "admin_silenciar": silenciar, "admin_banir": banir,
        "admin_desbanir": desbanir, "admin_fixar": fixar, "admin_desfixar": desfixar,
        "admin_enviar": enviartextocanal,
        "produtos": product_handlers.beneficiosprodutos,
        "bonusconstrutor": bonus_builder.bonus_construtor,
        "regras": rules.mostrar_regras,
        "marketingrede": marketing.marketing_rede,
        "recompensas2024": rewards.recompensas2024,
        "planificacao": planning.enviar_planificacao,
        "seguimento": kits.seguimento,
        "apresentacao": opportunity.apresentacaooportunidade,
        "fatorestransferencia": transfer_factors.fatorestransferencia,
        "fabrica4life": factory.fabrica4life,
        "folheteria": brochures.folheteria,
        "glossario": glossary.glossario,
        "convite": invites.mostrar_convites,
        "artes": art_creator.artes,
        "treinamento": training.treinamento,
        "ranking": ranking.mostrar_ranking,
        "leitura": reading_guide.leitura,
        "canais": channels.canais,
        "fidelidade": loyalty.fidelidade,
        "tabelas": tables.tabelas_menu,
        "usage_top": send_top_users_command,
        "usage_reset": reset_usage_data_command,
    }
    for command, handler in command_handlers.items():
        application.add_handler(CommandHandler(command, handler))

def register_callback_handlers(application: Application) -> None:
    """Registra o roteador principal de callbacks e handlers específicos."""
    application.add_handler(CallbackQueryHandler(
        welcome.welcome_callbacks_handler,
        pattern=f'^({welcome.CALLBACK_REGRAS}|{welcome.CALLBACK_INICIO}|{welcome.CALLBACK_MENU}|ajuda_.*)$'
    ))
    application.add_handler(CallbackQueryHandler(
        welcome.handle_verification_callback, pattern=f'^{welcome.VERIFY_MEMBER_CALLBACK}$'
    ))
    
    # Roteador principal para todos os outros callbacks
    application.add_handler(CallbackQueryHandler(callback_router))

def register_misc_handlers(application: Application) -> None:
    """Registra handlers de mensagem, agendamentos e outros."""
    
    # --- CORREÇÃO ---
    # A tarefa agendada foi comentada para evitar o conflito de 'event loop'.
    # if application.job_queue:
    #     application.job_queue.run_repeating(enviar_motivacao_agendada, interval=86400, first=0)
    
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.darboasvindas_handler))
    if CANAL_ID_2:
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)),
            welcome.handle_unverified_text_message
        ), group=2)
    application.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
        private_messaging.handle_private_message
    ), group=3)
    
    application.add_handler(get_file_id_handler(), group=0)
    application.add_handler(setup_group_id_handler())

async def main() -> None:
    """Ponto de entrada principal para iniciar o bot."""

    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        logger.warning("Locale 'pt_BR.UTF-8' não encontrado. Usando fallback.")

    if not BOT_TOKEN:
        logger.critical("CRITICAL: BOT_TOKEN não está definido!")
        return
        
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.bot_data['usage_tracker'] = UsageTracker()

    register_command_handlers(application)
    register_callback_handlers(application)
    register_misc_handlers(application)
    application.add_error_handler(error_handler)

    logger.info("Bot iniciado com sucesso. Aguardando updates...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())