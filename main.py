# NOME DO ARQUIVO: main.py
# REFACTOR: Ponto de entrada principal da aplicação. Orquestra a inicialização e o registro de todos os handlers.

import logging
import locale
import asyncio
from telegram import Update # Importação necessária adicionada
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
    welcome, rules, invites, events, channels, loyalty, private_messaging
)
from features.creative import art_creator
from features.general import start, help, bonus_builder
from features.products import handlers as product_handlers
from features.training import training, reading_guide
from features.user_tools import store_finder, prospect_list

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
    
    # Handlers de Conversa
    prospect_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("prospectos_add", prospect_list.adicionar_prospecto_conversa)],
        states={
            prospect_list.NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_nome)],
            prospect_list.TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_telefone)],
            prospect_list.CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_cidade)],
        },
        fallbacks=[CommandHandler("cancelar", prospect_list.cancelar_conversa)],
    )
    edit_prospect_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(prospect_list.editar_prospecto, pattern='^editar_')],
        states={
            prospect_list.EDITAR_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_nome_edicao)],
            prospect_list.EDITAR_TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_telefone_edicao)],
            prospect_list.EDITAR_CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prospect_list.capturar_cidade_edicao)],
        },
        fallbacks=[CommandHandler("cancelar", prospect_list.cancelar_conversa)],
    )
    application.add_handler(prospect_conv_handler)
    application.add_handler(edit_prospect_conv_handler)
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
        "eventos": events.escolher_local_evento,
        "prospectos_listar": prospect_list.listar_prospectos,
        "prospectos_relatorio": prospect_list.gerar_relatorio_comando,
        "prospectos_pdf": prospect_list.enviar_pdf,
        "usage_top": send_top_users_command,
        "usage_reset": reset_usage_data_command,
    }
    for command, handler in command_handlers.items():
        application.add_handler(CommandHandler(command, handler))

def register_callback_handlers(application: Application) -> None:
    """Registra o roteador principal de callbacks e handlers específicos."""
    # Handlers específicos que precisam ser registrados antes do roteador geral
    application.add_handler(CallbackQueryHandler(
        welcome.welcome_callbacks_handler,
        pattern=f'^({welcome.CALLBACK_REGRAS}|{welcome.CALLBACK_INICIO}|{welcome.CALLBACK_MENU}|ajuda_.*)$'
    ))
    application.add_handler(CallbackQueryHandler(
        welcome.handle_verification_callback, pattern=f'^{welcome.VERIFY_MEMBER_CALLBACK}$'
    ))
    # A LINHA ABAIXO FOI REMOVIDA POIS A FUNÇÃO 'confirmar_dados' NÃO EXISTE EM prospect_list.py
    # application.add_handler(CallbackQueryHandler(
    #     prospect_list.confirmar_dados, pattern='^confirmar$'
    # ))
    application.add_handler(CallbackQueryHandler(
        prospect_list.cancelar_conversa, pattern='^cancelar$'
    ))
    application.add_handler(CallbackQueryHandler(
        prospect_list.remover_prospecto, pattern='^remover_'
    ))
    
    # Roteador principal para todos os outros callbacks
    application.add_handler(CallbackQueryHandler(callback_router))

def register_misc_handlers(application: Application) -> None:
    """Registra handlers de mensagem, agendamentos e outros."""
    # Tarefa agendada
    if application.job_queue:
        application.job_queue.run_repeating(enviar_motivacao_agendada, interval=86400, first=0)
    
    # Handlers de Mensagem
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
    
    # Handlers de utilidade
    application.add_handler(get_file_id_handler(), group=0)
    application.add_handler(setup_group_id_handler())

async def main() -> None:
    """Ponto de entrada principal para iniciar o bot."""
    # Garante que a tabela de prospectos exista antes de iniciar
    await prospect_list.create_table_if_not_exists()

    # Configuração do Locale
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        logger.warning("Locale 'pt_BR.UTF-8' não encontrado. Usando fallback.")

    # Construção da Aplicação
    if not BOT_TOKEN:
        logger.critical("CRITICAL: BOT_TOKEN não está definido!")
        return
        
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Inicialização de dados do bot
    application.bot_data['usage_tracker'] = UsageTracker()

    # Registro de Handlers
    register_command_handlers(application)
    register_callback_handlers(application)
    register_misc_handlers(application)
    application.add_error_handler(error_handler)

    # Iniciar o Bot
    logger.info("Bot iniciado com sucesso. Aguardando updates...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())