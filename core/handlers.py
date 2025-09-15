# NOME DO ARQUIVO: core/handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

# --- Handlers de alto nível ---
from features.general.help_command import ajuda
from features.general.bonus_builder import callback_bonus_construtor
from features.products.handlers import products_callback_handler  # alias já existente

# Pacotes de negócios / comunidade / etc.
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

# --------------------------------------------------------------------------- #
# Dicionário de roteamento (prefixo → função)
# --------------------------------------------------------------------------- #
CALLBACK_ROUTING = {
    # Produtos
    'prod_': products_callback_handler,          # ← prefixo corrigido
    # Bônus-Construtor
    'bonusconstrutor_': callback_bonus_construtor,

    # Tabelas de preços
    'tabela_': tables.callback_tabelas,
    'preco_': tables.callback_tabelas,
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
# Roteador principal de callbacks
# --------------------------------------------------------------------------- #
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Distribui todas as callback queries para o handler adequado."""
    query = update.callback_query
    if not (query and query.data):
        return

    # Antiflood
    if not await check_flood(update):
        return

    callback_data = query.data