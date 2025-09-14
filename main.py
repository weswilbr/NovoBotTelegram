# NOME DO ARQUIVO: main.py
# REFACTOR: Ponto de entrada principal do bot, responsável por inicializar e registrar todos os handlers.

# --- Importações Padrão ---
import logging
import sys
import locale

# --- Importações do Telegram ---
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
from features.user_tools import prospect_list, store_finder

# --- Módulos de Utilitários (Utils) ---
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler
from utils.monitoring import commands as monitoring_commands
from utils.monitoring.motivation import enviar_motivacao_agendada
from utils.monitoring.tracker import UsageTracker

# --- Configuração do Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def register_command_handlers(app: Application) -> None:
    """Registra todos os CommandHandlers na aplicação."""
    command_handlers = {
        # Geral
        "start": start.start,
        "ajuda": help.ajuda,
        # Business
        "produtos": product_handlers.beneficiosprodutos,
        "bonusconstrutor": bonus_builder.bonus_construtor,
        "marketingrede": marketing.marketing_rede,
        "recompensas": rewards.mostrar_recompensas, # ATUALIZADO AQUI
        "apresentacao": opportunity.apresentacaooportunidade,
        "fatorestransferencia": transfer_factors.fatorestransferencia,
        "fabrica4life": factory.fabrica4life,
        "folheteria": brochures.folheteria,
        "glossario": glossary.glossario,
        "tabelas": tables.tabelas_menu,
        "planificacao": planning.enviar_planificacao,
        "ranking": ranking.mostrar_ranking,
        # Comunidade
        "regras": rules.mostrar_regras,
        "convite": invites.mostrar_convites,
        "canais": channels.canais,
        "fidelidade": loyalty.fidelidade,
        # Criativo e Treinamento
        "artes": art_creator.artes,
        "treinamento": training.treinamento,
        # Prospectos
        "listarprospectos": prospect_list.listar_prospectos,
        "relatorio": prospect_list.gerar_relatorio_comando,
        "pdf": prospect_list.enviar_pdf,
        # Admin
        "listaradmins": admin_commands.listar_admins,
        "silenciar": admin_commands.silenciar,
        "banir": admin_commands.banir,
        "desbanir": admin_commands.desbanir,
        "fixar": admin_commands.fixar,
        "desfixar": admin_commands.desfixar,
        "enviartextocanal": admin_commands.enviartextocanal,
        # Monitoramento
        "topusers": monitoring_commands.send_top_users_command,
        "resetusage": monitoring_commands.reset_usage_data_command,
    }
    for command, handler in command_handlers.items():
        app.add_handler(CommandHandler(command, handler))

    app.add_handler(store_finder.loja_handler)


def register_conversation_handlers(app: Application) -> None:
    """Registra todos os ConversationHandlers."""
    prospect_add_conv = ConversationHandler(
        entry_points=[CommandHandler("addprospecto", prospect_list.adicionar_prospecto_conversa)],
        states={
            prospect_list.NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_nome)],
            prospect_list.TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_telefone)],
            prospect_list.CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_cidade)],
        },
        fallbacks=[CommandHandler("cancelar", prospect_list.cancelar_conversa)],
    )
    prospect_edit_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(prospect_list.editar_prospecto, pattern='^editar_')],
        states={
            prospect_list.EDITAR_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_nome_edicao)],
            prospect_list.EDITAR_TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_telefone_edicao)],
            prospect_list.EDITAR_CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_cidade_edicao)],
        },
        fallbacks=[CommandHandler("cancelar", prospect_list.cancelar_conversa)],
    )
    app.add_handler(prospect_add_conv)
    app.add_handler(prospect_edit_conv)


def register_callback_handlers(app: Application) -> None:
    """Registra todos os CallbackQueryHandlers. A ordem importa!"""
    app.add_handler(CallbackQueryHandler(welcome.welcome_callbacks_handler, pattern=f'^({welcome.CALLBACK_REGRAS}|{welcome.CALLBACK_INICIO}|{welcome.CALLBACK_MENU}|ajuda_.*)$'))
    app.add_handler(CallbackQueryHandler(welcome.handle_verification_callback, pattern=f'^{welcome.VERIFY_MEMBER_CALLBACK}$'))
    app.add_handler(CallbackQueryHandler(brochures.brochures_callback_handler, pattern='^brochure_'))
    app.add_handler(CallbackQueryHandler(factory.factory_callback_handler, pattern='^factory_'))
    app.add_handler(CallbackQueryHandler(glossary.glossary_callback_handler, pattern='^glossary_'))
    app.add_handler(CallbackQueryHandler(marketing.marketing_callback_handler, pattern='^marketing_'))
    app.add_handler(CallbackQueryHandler(opportunity.opportunity_callback_handler, pattern='^opportunity_'))
    app.add_handler(CallbackQueryHandler(planning.planning_callback_handler, pattern='^planning_'))
    app.add_handler(CallbackQueryHandler(ranking.ranking_details_callback_handler, pattern='^ranking_details_'))
    app.add_handler(CallbackQueryHandler(tables.tables_callback_handler, pattern='^tables_')) # ATUALIZADO AQUI
    app.add_handler(CallbackQueryHandler(transfer_factors.transfer_factors_callback_handler, pattern='^tfactors_')) # ATUALIZADO AQUI
    
    # O roteador genérico deve ser o último.
    app.add_handler(CallbackQueryHandler(callback_router))


def register_message_handlers(app: Application) -> None:
    """Registra os handlers de mensagens e status."""
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome.darboasvindas_handler))
    if CANAL_ID_2:
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)), welcome.handle_unverified_text_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, private_messaging.handle_private_message))


def register_utility_handlers(app: Application) -> None:
    """Registra handlers de utilidade e o error handler."""
    app.add_handler(get_file_id_handler())
    app.add_handler(setup_group_id_handler())
    app.add_error_handler(error_handler)


def main() -> None:
    """Função principal que inicializa e executa o bot."""
    if not BOT_TOKEN:
        logger.critical("CRÍTICO: BOT_TOKEN não foi encontrado. O bot não pode iniciar.")
        sys.exit(1)
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        logger.warning("Locale 'pt_BR.UTF-8' não suportado. Usando locale padrão.")

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.bot_data['usage_tracker'] = UsageTracker()

    register_command_handlers(application)
    register_conversation_handlers(application)
    register_callback_handlers(application)
    register_message_handlers(application)
    register_utility_handlers(application)
    
    if application.job_queue:
        application.job_queue.run_repeating(enviar_motivacao_agendada, interval=86400, first=0)

    logger.info("Bot iniciado com sucesso. Aguardando atualizações...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()