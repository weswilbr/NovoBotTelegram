# NOME DO ARQUIVO: core/handlers.py
# REFACTOR: Roteador principal que direciona todas as queries de callback para seus handlers específicos.

import logging
from telegram import Update
from telegram.ext import ContextTypes

# --- Importação dos Módulos com Handlers de Callback ---
from features.business import (
    brochures, factory, glossary, marketing, opportunity,
    planning, ranking, tables, transfer_factors
)
from features.community import invites, channels, loyalty
from features.products import handlers as product_handlers
from features.training import training
from features.creative import art_creator
from features.general import bonus_builder

logger = logging.getLogger(__name__)


async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Roteador principal para todas as queries de callback não capturadas em main.py.
    """
    query = update.callback_query
    if not query or not query.data:
        return

    data = query.data
    logger.info(f"Callback roteado: '{data}' do usuário {query.from_user.id}")

    # --- Roteamento para Módulos Aprimorados ---
    if data.startswith(('brochure_', 'folheteria_')):
        await brochures.brochures_callback_handler(update, context)
    elif data.startswith('factory_'):
        await factory.factory_callback_handler(update, context)
    elif data.startswith('glossary_'):
        await glossary.glossary_callback_handler(update, context)
    elif data.startswith('marketing_'):
        await marketing.marketing_callback_handler(update, context)
    elif data.startswith('opportunity_'):
        await opportunity.opportunity_callback_handler(update, context)
    elif data.startswith('planning_'):
        await planning.planning_callback_handler(update, context)
    elif data.startswith('ranking_details_'):
        await ranking.ranking_details_callback_handler(update, context)
    elif data.startswith('tables_'):
        await tables.tables_callback_handler(update, context)
    elif data.startswith('tfactors_'):
        await transfer_factors.transfer_factors_callback_handler(update, context)
    elif data.startswith('bbuilder_'):
        await bonus_builder.bonus_builder_callback_handler(update, context)
    # CORREÇÃO APLICADA ABAIXO: Usando o novo handler e prefixo do módulo de Produtos.
    elif data.startswith('products_'):
        await product_handlers.products_callback_handler(update, context)

    # --- Roteamento para Módulos Não Refatorados (Mantendo Lógica Original) ---
    elif data.startswith('convite_'):
        await invites.enviar_convite(update, context)
    elif data == 'voltar_convites':
        await invites.mostrar_convites(update, context)
    elif data in ['youtube', 'telegram', 'whatsapp', 'voltar_canais']:
        await channels.handle_canais_callback(update, context)
    elif data.startswith('fidelidade_'):
        await loyalty.callback_fidelidade(update, context)
    elif data.startswith(('apoio', 'tutoriais', 'voltar')):
        await training.handle_treinamento_callback(update, context)
    elif data.startswith(('arte_', 'banner_', 'menu_', 'criativo_', 'voltar_menu_artes_principal')):
        await art_creator.button_callback(update, context)
        
    else:
        logger.warning(f"Nenhum handler no roteador principal para o callback: '{data}'")
        await query.answer("Este botão parece estar desatualizado ou não tem uma ação definida.", show_alert=True)