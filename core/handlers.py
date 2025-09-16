# NOME DO ARQUIVO: core/handlers.py
# Roteador central de callback-queries

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

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

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Mapa prefixo → função-handler
# (ordem importa: o primeiro prefixo que combinar será usado)
# --------------------------------------------------------------------------- #
CALLBACK_ROUTING = {
    # Produtos (menu principal + submenu)
    'prod_': products_callback_handler,

    # Bônus Construtor
    'bonusconstrutor_': callback_bonus_construtor,

    # Tabelas
    'tabela_': tables.callback_tabelas,
    'voltar_tabelas_principal': tables.callback_tabelas,

    # Marketing
    'baixar_video_marketing': marketing.callback_marketing_download,

    # Fábrica 4Life
    'fabrica_': factory.callback_fabrica4life,

    # Fatores de Transferência
    'fatorestransf_': transfer_factors.callback_fatorestransf_handler,

    # Folheteria
    'folheteria_': brochures.callback_folheteria,

    # Glossário
    'glossario_': glossary.callback_glossario,
    'baixar_glossario': glossary.callback_glossario,

    # Oportunidade
    'apresentacao_': opportunity.callback_apresentacao_oportunidade,

    # Ranking
    'detalhes_ranking_': ranking.enviar_detalhes_ranking,

    # Fidelidade
    'fidelidade_': loyalty.callback_fidelidade,

    # Convites
    'convite_': invites.enviar_convite,
    'voltar_convites': invites.mostrar_convites,

    # Canais
    'youtube': channels.handle_canais_callback,
    'telegram': channels.handle_canais_callback,
    'whatsapp': channels.handle_canais_callback,
    'voltar_canais': channels.handle_canais_callback,

    # Treinamento
    'apoio': training.handle_treinamento_callback,
    'tutoriais': training.handle_treinamento_callback,
    'voltar': training.handle_treinamento_callback,
    'apoio_': training.handle_treinamento_callback,
    'tutoriais_': training.handle_treinamento_callback,

    # Artes / Criativos
    'arte_': art_creator.button_callback,
    'banner_': art_creator.button_callback,
    'menu_': art_creator.button_callback,
    'criativo_': art_creator.button_callback,
    'voltar_menu_artes_principal': art_creator.button_callback,
}

# --------------------------------------------------------------------------- #
# Roteador principal
# --------------------------------------------------------------------------- #
async def callback_router(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not (query and query.data):
        return

    callback_data = query.data
    logger.info("Callback roteado: '%s'", callback_data)

    try:
        # encontra o primeiro prefixo que combina
        for prefix, handler in CALLBACK_ROUTING.items():
            if callback_data.startswith(prefix):
                await handler(update, context)
                break
        else:
            # nenhum prefixo encontrado → fallback /ajuda
            await query.answer()
            logger.warning("Nenhum handler para '%s'; exibindo ajuda.", callback_data)
            await ajuda(update, context)

    # ------------------------------------------------------------------- #
    except BadRequest as e:
        # ignora “message is not modified” e erros equivalentes
        if "message is not modified" not in str(e).lower():
            logger.error("BadRequest em '%s': %s", callback_data, e)

    except Exception as e:
        logger.error("Erro inesperado em '%s': %s", callback_data, e, exc_info=True)