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

logger = logging.getLogger(__name__)

# Dicionário de roteamento para todos os callbacks do bot
CALLBACK_ROUTING = {
    'products_': products_callback_handler,
    'bonusconstrutor_': callback_bonus_construtor,
    'tabela_': tables.callback_tabelas,
    'preco_': tables.callback_tabelas,
    'voltar_tabelas_principal': tables.callback_tabelas,
    'baixar_video_marketing': marketing.callback_marketing_download,
    'fabrica_': factory.callback_fabrica4life,
    'fatorestransf_': transfer_factors.callback_fatorestransf_handler,
    'folheteria_': brochures.callback_folheteria,
    'glossario_': glossary.callback_glossario,
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

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador principal para todas as queries de callback."""
    query = update.callback_query
    if not (query and query.data):
        return

    # Verifica se o usuário está clicando rápido demais
    if not await check_flood(update):
        return
    
    callback_data = query.data
    logger.info(f"Callback roteado: '{callback_data}'")

    try:
        handler_to_call = None
        # Procura o handler correspondente no dicionário de roteamento
        for prefix, handler in CALLBACK_ROUTING.items():
            if callback_data.startswith(prefix):
                handler_to_call = handler
                break

        if handler_to_call:
            await handler_to_call(update, context)
        else:
            # Se nenhum handler for encontrado, exibe a mensagem de ajuda como fallback
            await query.answer() # Adicionado aqui para o caso de fallback
            logger.warning(f"Nenhum handler no roteador para: '{callback_data}'. Exibindo ajuda.")
            await ajuda(update, context)

    except BadRequest as e:
        # Ignora o erro comum de "mensagem não modificada"
        if "message is not modified" not in str(e).lower():
            logger.error(f"Erro de BadRequest em '{callback_data}': {e}")
    except Exception as e:
        logger.error(f"Erro inesperado em '{callback_data}': {e}", exc_info=True)

