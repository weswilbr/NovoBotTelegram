# NOME DO ARQUIVO: core/handlers.py
# REFACTOR: Roteador principal que direciona todas as queries de callback para seus handlers específicos.

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

# Importa todos os handlers de callback das features
from features.general import help
from features.general.bonus_builder import callback_bonus_construtor
from features.products.handlers import callback_beneficios_handler
from features.business import (
    planning, tables, marketing, kits, factory,
    transfer_factors, brochures, glossary, opportunity, ranking
)
# CORREÇÃO: 'events' foi removido da linha de importação abaixo
from features.community import welcome, loyalty, invites, channels
# Funções de ConversationHandler (como confirmar_dados) não são importadas aqui,
# pois são gerenciadas pelo ConversationHandler no main.py.
from features.training import training, reading_guide
from features.creative import art_creator

from utils.anti_flood import check_flood
from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# Dicionário que mapeia prefixos de callback_data para as funções de handler correspondentes.
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
    'kit_': kits.handle_kit_choice,
    'armazem4life': factory.callback_fabrica4life,
    'envaseprodutos': factory.callback_fabrica4life,
    'novafabrica4life': factory.callback_fabrica4life,
    'fatorestransf_': transfer_factors.callback_fatorestransf_handler,
    'submenu_panfletos': brochures.callback_folheteria,
    'catalogo4life': brochures.callback_folheteria,
    'panfletoprodutosnovo': brochures.callback_folheteria,
    'panfletonovo4life': brochures.callback_folheteria,
    'submenu_enqueteimunidade': brochures.callback_folheteria,
    'voltar_menu_principal': brochures.callback_folheteria,
    'glossario': glossary.callback_glossario,
    'baixar_glossario': glossary.callback_glossario,
    'video_apresentacao': opportunity.callback_apresentacao_oportunidade,
    'link_plano_compacto': opportunity.callback_apresentacao_oportunidade,
    'arquivo_plano_compacto': opportunity.callback_apresentacao_oportunidade,
    'plano_completo_slide': opportunity.callback_apresentacao_oportunidade,
    'powerpoint_apresentacao': opportunity.callback_apresentacao_oportunidade,
    'arquivo_por_que_4life': opportunity.callback_apresentacao_oportunidade,
    'link_por_que_4life': opportunity.callback_apresentacao_oportunidade,
    'detalhes_ranking_': ranking.enviar_detalhes_ranking,
    # Community
    'welcome_': welcome.welcome_callbacks_handler,
    'verify_member': welcome.handle_verification_callback,
    # CORREÇÃO: A linha de roteamento de eventos foi removida abaixo
    # 'evento_': events.enviar_evento,
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

@group_member_required
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador principal para todas as queries de callback."""
    query = update.callback_query
    if not (query and query.data):
        return

    # Proteção contra múltiplos cliques rápidos
    if not await check_flood(update):
        return

    await query.answer()
    callback_data = query.data
    logger.info(f"Callback recebido: '{callback_data}' do usuário {query.from_user.id}")

    try:
        handler_to_call = None
        for prefix, handler in CALLBACK_ROUTING.items():
            if callback_data.startswith(prefix):
                handler_to_call = handler
                break
        
        # Callbacks de ConversationHandler (como 'remover_', 'confirmar', etc.)
        # são capturados pelo próprio ConversationHandler no main.py e não chegarão aqui.

        if handler_to_call:
            await handler_to_call(update, context)
        else:
            logger.warning(f"Nenhum handler encontrado para o callback: '{callback_data}'. Retornando ao menu de ajuda.")
            if update.effective_message:
                 await help.ajuda(update, context)

    except BadRequest as e:
        # Erro comum quando o usuário clica em um botão de uma mensagem antiga.
        if "message is not modified" not in str(e).lower():
            logger.error(f"Erro de BadRequest ao processar '{callback_data}': {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao processar '{callback_data}': {e}", exc_info=True)