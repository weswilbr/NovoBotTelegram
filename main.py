# NOME DO ARQUIVO: main.py
# REFACTOR: Ponto de entrada principal do bot, responsável por inicializar e registrar todos os handlers.
import logging
import sys
import locale
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

# --- Carregamento da Configuração ---
from config import BOT_TOKEN, CANAL_ID_2

# --- Handlers Principais ---
from core.handlers import callback_router
from features.admin.commands import (
    listar_admins, silenciar, banir, desbanir, fixar, desfixar, enviartextocanal
)
from features.community.private_messaging import handle_private_message
from features.community.welcome import (
    darboasvindas_handler, welcome_callbacks_handler, handle_verification_callback,
    handle_unverified_text_message, CALLBACK_REGRAS, CALLBACK_INICIO, CALLBACK_MENU,
    VERIFY_MEMBER_CALLBACK
)
from features.general.start import start
from features.general.help import ajuda
from features.user_tools.prospect_list import (
    adicionar_prospecto_conversa, listar_prospectos, gerar_relatorio_comando, enviar_pdf,
    cancelar_conversa, capturar_nome, capturar_telefone, capturar_cidade,
    editar_prospecto, capturar_nome_edicao, capturar_telefone_edicao, capturar_cidade_edicao,
    remover_prospecto, NOME, TELEFONE, CIDADE, EDITAR_NOME, EDITAR_TELEFONE, EDITAR_CIDADE
)
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler # <-- CORRIGIDO AQUI
from utils.monitoring.commands import send_top_users_command, reset_usage_data_command
from utils.monitoring.motivation import enviar_motivacao_agendada
from utils.monitoring.tracker import UsageTracker

# --- Mapeamento de Comandos ---
from features.business.opportunity import apresentacaooportunidade
from features.business.brochures import folheteria
from features.business.glossary import glossario
from features.products.handlers import beneficiosprodutos
from features.business.marketing import marketing_rede
from features.business.rewards import recompensas2024
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
from features.community.events import escolher_local_evento

# Configuração do Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Função principal que inicializa e executa o bot."""
    # Validação do Token
    if not BOT_TOKEN:
        logger.critical("CRITICAL: BOT_TOKEN não foi encontrado. O bot não pode iniciar.")
        sys.exit(1)

    # Configuração do Locale
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        logger.warning("Locale 'pt_BR.UTF-8' não encontrado. Usando fallback.")

    # Construtor da Aplicação
    builder = ApplicationBuilder().token(BOT_TOKEN)
    application = builder.build()

    # Armazena o tracker no bot_data
    application.bot_data['usage_tracker'] = UsageTracker()

    # --- Handlers de Conversa ---
    prospect_list_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addprospecto", adicionar_prospecto_conversa)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_nome)],
            TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_telefone)],
            CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_cidade)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar_conversa)],
    )
    edit_prospect_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(editar_prospecto, pattern='^editar_')],
        states={
            EDITAR_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_nome_edicao)],
            EDITAR_TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_telefone_edicao)],
            EDITAR_CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_cidade_edicao)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar_conversa)],
    )

    # --- Registro de Handlers ---
    # Comandos
    command_handlers = {
        "start": start, "ajuda": ajuda, "produtos": beneficiosprodutos,
        "apresentacaooportunidade": apresentacaooportunidade, "folheteria": folheteria,
        "glossario": glossario, "marketingrede": marketing_rede, "recompensas2024": recompensas2024,
        "fatorestransferencia": fatorestransferencia, "fabrica4life": fabrica4life,
        "bonusconstrutor": bonus_construtor, "regras": mostrar_regras, "convite": mostrar_convites,
        "artes": artes, "treinamento": treinamento, "ranking": mostrar_ranking, "canais": canais,
        "fidelidade": fidelidade, "tabelas": tabelas_menu, "eventos": escolher_local_evento,
        "listarprospectos": listar_prospectos, "relatorio": gerar_relatorio_comando, "pdf": enviar_pdf,
        "topusers": send_top_users_command, "resetusage": reset_usage_data_command,
        "listaradmins": listar_admins, "silenciar": silenciar, "banir": banir,
        "desbanir": desbanir, "fixar": fixar, "desfixar": desfixar,
        "enviartextocanal": enviartextocanal
    }
    for command, handler in command_handlers.items():
        application.add_handler(CommandHandler(command, handler))

    # Handlers de Conversa
    application.add_handler(prospect_list_conv_handler)
    application.add_handler(edit_prospect_conv_handler)

    # Callbacks
    application.add_handler(CallbackQueryHandler(welcome_callbacks_handler, pattern=f'^({CALLBACK_REGRAS}|{CALLBACK_INICIO}|{CALLBACK_MENU}|ajuda_.*)$'))
    application.add_handler(CallbackQueryHandler(handle_verification_callback, pattern=f'^{VERIFY_MEMBER_CALLBACK}$'))
    application.add_handler(CallbackQueryHandler(callback_router)) # Roteador genérico

    # Mensagens
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, darboasvindas_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, handle_private_message))
    if CANAL_ID_2:
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=int(CANAL_ID_2)), handle_unverified_text_message))

    # Outros Handlers
    application.add_handler(get_file_id_handler())
    application.add_handler(setup_group_id_handler()) # <-- CORRIGIDO AQUI
    application.add_error_handler(error_handler)

    # Tarefas Agendadas
    if application.job_queue:
        application.job_queue.run_repeating(enviar_motivacao_agendada, interval=86400, first=0)

    # Iniciar o Bot
    logger.info("Bot iniciado com sucesso. Aguardando updates...")
    application.run_polling()

if __name__ == '__main__':
    main()

