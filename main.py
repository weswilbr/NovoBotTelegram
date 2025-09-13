# NOME DO ARQUIVO: main.py
# REFACTOR: Ponto de entrada principal do bot, responsável por inicializar e registrar todos os handlers.

# --- Importações Padrão ---
import logging
import sys
import locale

# --- Importações do Telegram ---
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
# É uma ótima prática isolar as configurações, como tokens e IDs.
from config import BOT_TOKEN, CANAL_ID_2

# --- Handlers da Aplicação ---
# A estrutura modularizada com handlers em seus próprios diretórios é excelente.
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

# --- Utilitários ---
from utils.error_handler import error_handler
from utils.get_file_id import get_file_id_handler
from utils.get_group_id import setup_group_id_handler
from utils.monitoring.commands import send_top_users_command, reset_usage_data_command
from utils.monitoring.motivation import enviar_motivacao_agendada
from utils.monitoring.tracker import UsageTracker

# --- Configuração do Logging ---
# Essencial para depuração e monitoramento do bot em produção.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Função principal que inicializa e executa o bot."""
    # Validação do Token do Bot
    if not BOT_TOKEN:
        logger.critical("CRÍTICO: A variável BOT_TOKEN não foi encontrada. O bot não pode iniciar.")
        sys.exit(1)

    # Configuração de Localização para o Brasil (datas, moeda, etc.)
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        logger.warning("Locale 'pt_BR.UTF-8' não suportado no sistema. Usando o locale padrão.")

    # Construtor da Aplicação
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Inicializa e armazena o tracker de uso no contexto do bot
    application.bot_data['usage_tracker'] = UsageTracker()

    # --- Definição de Handlers de Conversa ---
    # Usar ConversationHandler é a forma correta de lidar com diálogos de múltiplos passos.
    prospect_list_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addprospecto", adicionar_prospecto_conversa)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_nome)],
            TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_telefone)],
            CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_cidade)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar_conversa)],
        per_user=True # Garante que conversas de diferentes usuários não se misturem
    )

    edit_prospect_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(editar_prospecto, pattern='^editar_')],
        states={
            EDITAR_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_nome_edicao)],
            EDITAR_TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_telefone_edicao)],
            EDITAR_CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_cidade_edicao)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar_conversa)],
        per_user=True # Garante que conversas de diferentes usuários não se misturem
    )

    # --- Registro de Handlers na Aplicação ---

    # 1. Comandos: Usar um dicionário para registrar comandos torna o código mais limpo e escalável.
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

    # 2. Handlers de Conversa
    application.add_handler(prospect_list_conv_handler)
    application.add_handler(edit_prospect_conv_handler)

    # 3. Callbacks de Botões Inline
    # Handlers mais específicos (com padrões mais restritos) devem vir primeiro.
    application.add_handler(CallbackQueryHandler(welcome_callbacks_handler, pattern=f'^({CALLBACK_REGRAS}|{CALLBACK_INICIO}|{CALLBACK_MENU}|ajuda_.*)$'))
    application.add_handler(CallbackQueryHandler(handle_verification_callback, pattern=f'^{VERIFY_MEMBER_CALLBACK}$'))
    application.add_handler(CallbackQueryHandler(callback_router)) # Roteador genérico por último

    # 4. Handlers de Mensagem
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, darboasvindas_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, handle_private_message))
    
    # Adiciona handler para mensagens em um canal específico apenas se o ID estiver configurado.
    if CANAL_ID_2:
        try:
            channel_id = int(CANAL_ID_2)
            application.add_handler(MessageHandler(
                filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=channel_id), 
                handle_unverified_text_message
            ))
        except ValueError:
            logger.error(f"A variável CANAL_ID_2 ('{CANAL_ID_2}') não é um ID de chat válido.")

    # 5. Handlers Utilitários
    application.add_handler(get_file_id_handler())
    application.add_handler(setup_group_id_handler())
    application.add_error_handler(error_handler) # Essencial para capturar e logar erros

    # --- Tarefas Agendadas (Jobs) ---
    # Verifica se a Job Queue está disponível antes de agendar tarefas.
    if application.job_queue:
        # Envia uma mensagem a cada 24 horas (86400 segundos).
        application.job_queue.run_repeating(enviar_motivacao_agendada, interval=86400, first=0)

    # --- Iniciar o Bot ---
    logger.info("Bot iniciado com sucesso. Aguardando atualizações...")
    application.run_polling()

if __name__ == '__main__':
    main()