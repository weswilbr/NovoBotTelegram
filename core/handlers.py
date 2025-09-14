# NOME DO ARQUIVO: core/handlers.py
# REFACTOR: Roteador de callbacks limpo, com todas as referências a códigos antigos removidas.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

# --- Imports Corrigidos e Limpos ---
# A função 'ajuda' agora é importada do local correto.
from features.general.help_command import ajuda
from features.general.bonus_builder import callback_bonus_construtor
from features.products.handlers import callback_beneficios_handler
from features.business import (
    planning, tables, marketing, factory,
    transfer_factors, brochures, glossary, opportunity, ranking
)
from features.community import loyalty, invites, channels
from features.training import training, reading_guide
from features.creative import art_creator

# Utilitários
from utils.anti_flood import check_flood
# LINHA CORRIGIDA ABAIXO
from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# Dicionário de roteamento limpo, sem funcionalidades removidas
CALLBACK_ROUTING = {
    # General
    'bonusconstrutor_': callback_bonus_construtor,
    # Products
    'beneficio': callback_beneficios_handler,
    'produtos_individuais': callback_beneficios_handler,
    'voltar_produtos': callback_beneficios_handler,
    # Business
    'planotrabalho90dias_': planning.callback_planificacao,
    'tabela_': tables.callback_tabelas,
    'preco_': tables.callback_tabelas,
    'voltar_tabelas_principal': tables.callback_tabelas,
    'baixar_video_marketing': marketing.handle_download_callback,
    'fabrica_': factory.callback_fabrica4life,
    'fatorestransf_': transfer_factors.callback_fatorestransf_handler,
    'folheteria_': brochures.callback_folheteria,
    'glossario': glossary.callback_glossario,
    'baixar_glossario': glossary.callback_glossario,
    'apresentacao_': opportunity.callback_apresentacao_oportunidade,
    'detalhes_ranking_': ranking.enviar_detalhes_ranking,
    # Community
    'fidelidade_': loyalty.callback_fidelidade,
    'convite_': invites.enviar_convite,
    'voltar_convites': invites.mostrar_convites,
    'youtube': channels.handle_canais_callback,
    'telegram': channels.handle_canais_callback,
    'whatsapp': channels.handle_canais_callback,
    'voltar_canais': channels.handle_canais_callback,
    # Training
    'apoio': training.handle_treinamento_callback,
    'tutoriais': training.handle_treinamento_callback,
    'voltar': training.handle_treinamento_callback,
    'apoio_': training.handle_treinamento_callback,
    'tutoriais_': training.handle_treinamento_callback,
    'guia_exito_': reading_guide.callback_leitura,
    # Creative
    'arte_': art_creator.button_callback,
    'banner_': art_creator.button_callback,
    'menu_': art_creator.button_callback,
    'criativo_': art_creator.button_callback,
    'voltar_menu_artes_principal': art_creator.button_callback,
}

# NOTA: Os callbacks de 'welcome' foram removidos daqui porque já são
# tratados por um handler mais específico no main.py, evitando redundância.

@group_member_required
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador principal para todas as queries de callback que não foram capturadas por handlers mais específicos."""
    query = update.callback_query
    if not (query and query.data): return

    # Verifica anti-flood antes de processar
    if not await check_flood(update): return

    await query.answer()
    callback_data = query.data
    logger.info(f"Callback roteado via core/handlers: '{callback_data}'")

    try:
        handler_to_call = None
        # Encontra o handler correspondente ao prefixo do callback
        for prefix, handler in CALLBACK_ROUTING.items():
            if callback_data.startswith(prefix):
                handler_to_call = handler
                break

        if handler_to_call:
            await handler_to_call(update, context)
        else:
            # Se nenhum handler for encontrado, exibe o menu de ajuda como fallback
            logger.warning(f"Nenhum handler no roteador para: '{callback_data}'. Exibindo ajuda.")
            # Chamada corrigida para a função 'ajuda'
            await ajuda(update, context)

    except BadRequest as e:
        # Ignora o erro "message is not modified" que é comum e inofensivo
        if "message is not modified" not in str(e).lower():
            logger.error(f"Erro de BadRequest em '{callback_data}': {e}")
    except Exception as e:
        logger.error(f"Erro inesperado em '{callback_data}': {e}", exc_info=True)

