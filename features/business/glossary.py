# NOME DO ARQUIVO: features/business/glossary.py
# REFACTOR: Gerencia a exibição e o download do glossário de termos.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from features.products.data import MEDIA
from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# --- Dicionário de Termos ---
# Manter os termos aqui torna o módulo autossuficiente e fácil de atualizar.
GLOSSARY_TERMS = {
    'upline': ('🔝 Upline', '**🔝 Upline:** A linha de Afiliados diretamente acima de você.'),
    'matriculador': ('👤 Matriculador', '**👤 Matriculador:** A pessoa que apresentou a 4Life para você (pode ser também o seu patrocinador).'),
    'patrocinador': ('🧑‍💼 Patrocinador', '**🧑‍💼 Patrocinador:** A pessoa em sua linha upline que está diretamente acima de você.'),
    'volume_equipe': ('📈 Volume Equipe', '**📈 Volume Equipe:** O Volume Principal, mais os pedidos de sua linha frontal.'),
    'linha_frontal': ('👥 Linha Frontal', '**👥 Linha Frontal:** Seu primeiro nível de Clientes Preferenciais e Afiliados que você patrocinou.'),
    'volume_tres_niveis': ('🔢 Volume Três Níveis', '**🔢 Volume Três Níveis:** Composto pelo seu Volume Principal (PV) e o PV das pessoas em seus três primeiros níveis.'),
    'clientes_varejo': ('🛒 Clientes Varejo', '**🛒 Clientes Varejo:** Clientes que compram os produtos da 4Life no preço de varejo.'),
    'clientes_preferenciais': ('🏷️ Clientes Preferenciais', '**🏷️ Clientes Preferenciais:** Clientes que se inscrevem para comprar produtos 4Life a preços de atacado.'),
    'downline': ('⬇️ Downline', '**⬇️ Downline:** A linha de Afiliados e Clientes Preferenciais que ficam diretamente abaixo de você.'),
    'perna': ('📊 Perna', '**📊 Perna:** Uma parte de seus downlines que começa com uma pessoa de sua linha frontal.'),
    'lp': ('💰 Life Points (LP)', '**💰 Life Points (LP):** Valor em pontos atribuído a cada produto, usado para calcular comissões.'),
    'pv': ('🏦 Volume Principal (PV)', '**🏦 Volume Principal (PV):** O total de LP dos produtos comprados por você.'),
    'vo': ('📊 Volume Organizacional (VO)', '**📊 Volume Organizacional (VO):** Os LP de suas compras, clientes e todos em sua downline.'),
    'bonus_rapido': ('💸 Bônus Rápido', '**💸 Bônus Rápido:** Comissão de 25% sobre o primeiro pedido de cada novo Cliente Preferencial.'),
    'programa_fidelidade': ('🎁 Programa Fidelidade', '**🎁 Programa Fidelidade:** Recompensa clientes mensais com 15% em Pontos de Fidelidade.'),
    'compressao': ('🔄 Compressão', '**🔄 Compressão:** Afiliados não qualificados não são contados no cálculo de comissões.'),
    'bonus_builder': ('🏆 Bônus Builder', '**🏆 Bônus Builder:** Bônus para incentivar Afiliados a inscrever e reter sua rede.')
}

def get_glossary_menu() -> InlineKeyboardMarkup:
    """Gera dinamicamente o teclado do glossário a partir do dicionário de termos."""
    buttons = []
    row = []
    # Itera sobre os termos para criar os botões
    for key, (label, _) in GLOSSARY_TERMS.items():
        row.append(InlineKeyboardButton(label, callback_data=f'glossary_showterm_{key}'))
        # Agrupa os botões em linhas de 2
        if len(row) == 2:
            buttons.append(row)
            row = []
    # Adiciona a última linha se ela tiver um número ímpar de botões
    if row:
        buttons.append(row)
    
    # Adiciona o botão de download e o de fechar
    buttons.append([InlineKeyboardButton("📥 Baixar Glossário Completo (.pdf)", callback_data='glossary_download')])
    return InlineKeyboardMarkup(buttons)

async def _show_main_menu(update: Update) -> None:
    """Função auxiliar para exibir ou editar para o menu principal do glossário."""
    text = "📖 *Glossário de Termos*\n\nSelecione um termo para ver sua definição ou baixe o arquivo completo."
    keyboard = get_glossary_menu()
    
    # Se for uma callback (ex: vindo do botão "Voltar"), edita a mensagem.
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode='Markdown')
    # Se for um comando (/glossario), envia uma nova mensagem.
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

@group_member_required
async def glossario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /glossario. Exibe o menu principal."""
    await _show_main_menu(update)

async def _show_term_definition(query: Update.callback_query, term_key: str) -> None:
    """Exibe a definição de um termo específico."""
    _, definition = GLOSSARY_TERMS.get(term_key, (None, None))
    if not definition:
        await query.edit_message_text("⚠️ Termo não encontrado.")
        return

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar ao Glossário", callback_data='glossary_main')]])
    await query.edit_message_text(f"{definition}", reply_markup=keyboard, parse_mode='Markdown')

async def _download_glossary(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o documento completo do glossário."""
    document_id = MEDIA.get('glossario', {}).get('documento')

    if not document_id:
        await query.answer("⚠️ Arquivo não disponível no momento.", show_alert=True)
        return

    try:
        await context.bot.send_document(chat_id=query.message.chat.id, document=document_id)
        # Edita a mensagem original para confirmar o envio e remover os botões.
        await query.edit_message_text("✅ Glossário enviado! Verifique o documento acima.", reply_markup=None)
    except TelegramError as e:
        logger.error(f"Erro ao enviar glossário (ID: {document_id}): {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o arquivo. Tente novamente mais tarde.", show_alert=True)


async def glossary_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador para todos os callbacks que começam com 'glossary_'."""
    query = update.callback_query
    await query.answer()
    
    data = query.data

    if data.startswith('glossary_showterm_'):
        term_key = data.split('_', 2)[2]
        await _show_term_definition(query, term_key)
    elif data == 'glossary_download':
        await _download_glossary(query, context)
    elif data == 'glossary_main':
        await _show_main_menu(update)

# NOTA PARA INTEGRAÇÃO EM main.py:
# Adicionar:
# from features.business import glossary
# application.add_handler(CallbackQueryHandler(glossary.glossary_callback_handler, pattern='^glossary_'))