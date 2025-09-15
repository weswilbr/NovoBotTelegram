# NOME DO ARQUIVO: core/handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

# --- Imports Corrigidos e Limpos ---
from features.general.help_command import ajuda
from features.general.bonus_builder import callback_bonus_construtor
from features.products.handlers import products_callback_handler
from features.business import (
    tables, marketing, factory,
    transfer_factors, brochures, glossary, opportunity, ranking
)
from features.community import loyalty, invites, channels
from features.training import training
from features.creative import art_creator

# Utilitários
from utils.anti_flood import check_flood
# CORREÇÃO: A linha abaixo foi removida, pois o ficheiro já não existe.
# from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# Dicionário de roteamento simplificado
CALLBACK_ROUTING = {
    # ... (o conteúdo do dicionário permanece o mesmo)
    'products_': products_callback_handler,
    'bonusconstrutor_': callback_bonus_construtor,
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
    'fidelidade_': loyalty.callback_fidelidade,
    'convite_': invites.enviar_convite,
    'voltar_convites': invites.mostrar_convites,
    'youtube': channels.handle_canais_callback,
    'telegram': channels.handle_canais_callback,
    'whatsapp': channels.handle_canais_callback,
    'voltar_canais': channels.handle_canais_callback,
    'apoio': training.handle_treinamento_callback,
    'tutoriais': training.handle_treinamento_callback,
    'voltar': training.handle_treinamento_callback,
    'apoio_': training.handle_treinamento_callback,
    'tutoriais_': training.handle_treinamento_callback,
    'arte_': art_creator.button_callback,
    'banner_': art_creator.button_callback,
    'menu_': art_creator.button_callback,
    'criativo_': art_creator.button_callback,
    'voltar_menu_artes_principal': art_creator.button_callback,
}

# CORREÇÃO: O decorador @group_member_required foi removido da função abaixo.
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador principal para todas as queries de callback."""
    query = update.callback_query
    if not (query and query.data): return

    if not await check_flood(update): return

    await query.answer()
    callback_data = query.data
    logger.info(f"Callback roteado: '{callback_data}'")

    try:
        handler_to_call = None
        for prefix, handler in CALLBACK_ROUTING.items():
            if callback_data.startswith(prefix):
                handler_to_call = handler
                break

        if handler_to_call:
            await handler_to_call(update, context)
        else:
            logger.warning(f"Nenhum handler no roteador para: '{callback_data}'. Exibindo ajuda.")
            await ajuda(update, context)

    except BadRequest as e:
        if "message is not modified" not in str(e).lower():
            logger.error(f"Erro de BadRequest em '{callback_data}': {e}")
    except Exception as e:
        logger.error(f"Erro inesperado em '{callback_data}': {e}", exc_info=True)