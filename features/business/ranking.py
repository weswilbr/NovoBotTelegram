# NOME DO ARQUIVO: features/business/ranking.py
# REFACTOR: Gerencia a lógica para exibir o ranking de posições e seus detalhes.

import locale
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from telegram.ext import ContextTypes

# Importa o dicionário de dados do arquivo irmão na mesma pasta.
from .ranking_data import POSITIONS

logger = logging.getLogger(__name__)

# --- Funções de Formatação ---

def _format_currency(value: float | int | None) -> str:
    """
    Formata um valor numérico como moeda (R$).
    Tenta usar o locale 'pt_BR' para uma formatação ideal. Se falhar (por exemplo,
    se o locale não estiver instalado no servidor), usa um método manual como fallback.
    """
    if not isinstance(value, (int, float)):
        return _format_value(value)
    try:
        # Tenta usar o locale configurado em main.py
        return locale.currency(value, grouping=True, symbol='R$')
    except (locale.Error, TypeError, ValueError):
        # Fallback: Formatação manual para o padrão brasileiro (ex: R$ 1.234,56)
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def _format_value(value, prefix: str = "", suffix: str = "") -> str:
    """Formata um valor genérico para exibição, tratando None como 'N/A'."""
    if value is None:
        return "N/A"
    if isinstance(value, (int, float)):
        try:
            # Tenta usar formatação de número com separador de milhar do locale
            return f"{prefix}{value:n}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (locale.Error, ValueError):
            # Fallback sem locale
             return f"{prefix}{value:,}{suffix}"
    return str(value)

def _format_position_details(position_name: str, position_data: dict) -> str:
    """
    Cria a mensagem de texto formatada com os detalhes de uma posição.
    Isso separa a lógica de apresentação da lógica do handler.
    """
    # Formata a lista de linhas qualificadas de forma legível
    linhas_qualificadas_str = "N/A"
    if position_data.get('linhas_qualificadas'):
        linhas_list = [f"{item['quantidade']} {item['posicao']}" for item in position_data['linhas_qualificadas']]
        linhas_qualificadas_str = ", ".join(linhas_list)

    # Constrói a mensagem final usando f-strings e as funções de formatação
    return "\n".join([
        f"{position_data.get('emoji', '▫️')} *{position_name}* - _{position_data.get('nivel_categoria', 'N/A')}_",
        "", "📋 *Requisitos:*",
        f"• PV Mensal: *{_format_value(position_data.get('pv_mensal'), suffix=' PV')}*",
        f"• Inscritos Pessoais: *{_format_value(position_data.get('inscritos_pessoais'))}*",
        f"• LP nos 3 Níveis: *{_format_value(position_data.get('lp_nos_3_niveis'), suffix=' LP')}*",
        f"• Linhas Qualificadas: *{linhas_qualificadas_str}*",
        f"• Volume Organizacional: *{_format_value(position_data.get('vo_rede'), suffix=' VO')}*",
        "", "💰 *Ganhos e Benefícios:*",
        f"• Média de Ganhos: *{_format_currency(position_data.get('media_ganho'))}*",
        f"• Bônus de Participação: *{_format_currency(position_data.get('bonus_participacao'))}*",
        f"• Viagens de Incentivo: *{'Sim ✅' if position_data.get('viagens_incentivo') else 'Não ❌'}*",
        "", "📌 *Observação:*",
        f"_{position_data.get('observacao', 'Nenhuma.')}_"
    ])

# --- Handlers ---

async def mostrar_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler do comando /ranking.
    Exibe um menu com todas as posições do ranking para o usuário selecionar.
    """
    if not update.message:
        return

    # Gera o teclado dinamicamente a partir do dicionário POSITIONS
    keyboard = [
        [InlineKeyboardButton(f"{details.get('emoji', '▫️')} {name}", callback_data=f"ranking_details_{name}")]
        for name, details in POSITIONS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💎 *Ranking de Posições*\n\n"
        "Selecione uma posição para receber todos os detalhes no seu privado.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def ranking_details_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Lida com os callbacks do menu de ranking.
    Envia os detalhes de uma posição específica no privado do usuário.
    """
    query = update.callback_query
    if not query or not query.from_user or not context.bot:
        return

    # Extrai o nome da posição do callback_data. Ex: 'ranking_details_Diamond' -> 'Diamond'
    position_name = query.data.split("ranking_details_")[1]
    position_data = POSITIONS.get(position_name)

    if not position_data:
        await query.answer("❌ Posição não encontrada. Por favor, tente novamente.", show_alert=True)
        return

    # Gera a mensagem formatada chamando a função auxiliar
    message_text = _format_position_details(position_name, position_data)
    
    try:
        # Tenta enviar a mensagem para o chat privado do usuário
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=message_text,
            parse_mode="Markdown"
        )
        await query.answer("✅ Detalhes enviados no seu privado!")
    except error.Forbidden:
        # Erro clássico: o bot não pode iniciar uma conversa.
        # Informa ao usuário exatamente como resolver o problema.
        bot_username = context.bot.username
        await query.answer(
            f"Preciso que você me inicie no privado primeiro! Clique aqui: t.me/{bot_username}",
            show_alert=True
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar detalhes do ranking para {query.from_user.id}: {e}")
        await query.answer("Ocorreu um erro ao enviar os detalhes. Tente novamente.", show_alert=True)

# NOTA PARA INTEGRAÇÃO EM main.py:
# Este módulo exporta dois handlers que precisam ser registrados:
# 1. O comando para mostrar o menu.
# 2. O callback para lidar com os cliques nos botões.
#
# Adicionar:
# from features.business import ranking
#
# Em register_command_handlers:
# "ranking": ranking.mostrar_ranking,
#
# Em register_callback_handlers:
# application.add_handler(CallbackQueryHandler(ranking.ranking_details_callback_handler, pattern='^ranking_details_'))