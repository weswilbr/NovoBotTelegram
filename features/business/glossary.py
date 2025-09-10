# NOME DO ARQUIVO: features/business/glossary.py
# REFACTOR: Gerencia a exibição e o download do glossário de termos.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from features.products.data import MEDIA  # Apenas MEDIA é necessário daqui
from utils.verification import group_member_required
from utils.anti_flood import check_flood

logger = logging.getLogger(__name__)

# Os termos do glossário foram movidos para este arquivo para torná-lo autossuficiente.
GLOSSARIO_TERMS = {
    'upline': '**🔝 Upline:** A linha de Afiliados diretamente acima de você.',
    'matriculador': '**👤 Matriculador:** A pessoa que apresentou a 4Life para você (pode ser também o seu patrocinador).',
    'patrocinador': '**🧑‍💼 Patrocinador:** A pessoa em sua linha upline que está diretamente acima de você (pode ser também a pessoa que fez sua inscrição).',
    'volume_equipe': '**📈 Volume Equipe:** O Volume Principal, mais os pedidos de sua linha frontal de Clientes Preferenciais e Afiliados.',
    'linha_frontal': '**👥 Linha Frontal:** Seu primeiro nível de Clientes Preferenciais e Afiliados que você patrocinou.',
    'volume_tres_niveis': '**🔢 Volume Três Níveis:** Composto pelo total de seu Volume Principal (PV) e o PV combinado das pessoas em seus três primeiros níveis.',
    'clientes_varejo': '**🛒 Clientes Varejo:** Clientes que compram os produtos da 4Life no preço de varejo.',
    'clientes_preferenciais': '**🏷️ Clientes Preferenciais:** Clientes que se inscrevem para comprar produtos 4Life a preços de atacado.',
    'downline': '**⬇️ Downline:** A linha de Afiliados e Clientes Preferenciais que ficam diretamente abaixo de você.',
    'perna': '**📊 Perna:** Uma parte de seus downlines que começa com uma pessoa de sua linha frontal e continua abaixo daquele Afiliado.',
    'lp': '**💰 Life Points (LP):** Valor em pontos atribuído a cada produto da 4Life, usado para calcular comissões.',
    'pv': '**🏦 Volume Principal (PV):** O total de LP dos produtos comprados por você, para consumo próprio ou para venda a varejo.',
    'vo': '**📊 Volume Organizacional (VO):** Os LP de suas compras pessoais, clientes e todos os Afiliados e clientes em sua downline.',
    'bonus_rapido': '**💸 Bônus Rápido:** Comissão de 25% sobre o primeiro pedido de cada novo Cliente Preferencial inscrito pessoalmente.',
    'programa_fidelidade': '**🎁 Programa Fidelidade:** Recompensa Afiliados e Clientes Preferenciais que compram mensalmente com 15% em Pontos de Fidelidade.',
    'compressao': '**🔄 Compressão:** Afiliados que não se qualificam não são contados no cálculo de comissões.',
    'bonus_builder': '**🏆 Bônus Builder:** Bônus para incentivar Afiliados a inscrever novos clientes e reter sua rede.'
}


@group_member_required
async def glossario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal do glossário."""
    keyboard = [
        [InlineKeyboardButton("🔝 Upline", callback_data='glossario_upline'), InlineKeyboardButton("👤 Matriculador", callback_data='glossario_matriculador')],
        [InlineKeyboardButton("🧑‍💼 Patrocinador", callback_data='glossario_patrocinador'), InlineKeyboardButton("📈 Volume Equipe", callback_data='glossario_volume_equipe')],
        [InlineKeyboardButton("👥 Linha Frontal", callback_data='glossario_linha_frontal'), InlineKeyboardButton("🔢 Volume Três Níveis", callback_data='glossario_volume_tres_niveis')],
        [InlineKeyboardButton("🛒 Clientes Varejo", callback_data='glossario_clientes_varejo'), InlineKeyboardButton("🏷️ Clientes Preferenciais", callback_data='glossario_clientes_preferenciais')],
        [InlineKeyboardButton("⬇️ Downline", callback_data='glossario_downline'), InlineKeyboardButton("📊 Perna", callback_data='glossario_perna')],
        [InlineKeyboardButton("💰 Life Points (LP)", callback_data='glossario_lp'), InlineKeyboardButton("🏦 Volume Principal (PV)", callback_data='glossario_pv')],
        [InlineKeyboardButton("📊 Volume Organizacional (VO)", callback_data='glossario_vo'), InlineKeyboardButton("💸 Bônus Rápido", callback_data='glossario_bonus_rapido')],
        [InlineKeyboardButton("🎁 Programa Fidelidade", callback_data='glossario_programa_fidelidade'), InlineKeyboardButton("🔄 Compressão", callback_data='glossario_compressao')],
        [InlineKeyboardButton("🏆 Bônus Builder", callback_data='glossario_bonus_builder')],
        [InlineKeyboardButton("📥 Baixar Glossário Completo", callback_data='baixar_glossario')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "Escolha um termo do glossário ou baixe o glossário completo:"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


@group_member_required
async def callback_glossario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com as seleções do menu do glossário."""
    query = update.callback_query
    if not query or not query.data: return

    if not await check_flood(update): return
    
    await query.answer()
    callback_data = query.data
    
    termo_key = callback_data.replace('glossario_', '')

    if termo_key in GLOSSARIO_TERMS:
        keyboard = [[InlineKeyboardButton("🔙 Voltar ao Glossário", callback_data='glossario')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"{GLOSSARIO_TERMS[termo_key]}\n\nEscolha outro termo ou volte.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif callback_data == 'baixar_glossario':
        documento_id = MEDIA.get('glossario', {}).get('documento')
        if documento_id:
            await context.bot.send_document(chat_id=query.message.chat.id, document=documento_id)
        else:
            await query.message.reply_text("⚠️ Arquivo do glossário não encontrado.")
    elif callback_data == 'glossario':
        await glossario(update, context)

