# NOME DO ARQUIVO: features/community/invites.py
# REFACTOR: Gerencia a exibição e o envio de modelos de convite.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# Os textos dos convites foram movidos para este arquivo para torná-lo autossuficiente.
CONVITES_TEXT = {
    'convite_1': (
        "📈 Convite Profissional\n\n"
        "Oi [Nome do Convidado], tudo bem? Estou trabalhando em um projeto que está dando super certo e lembrei de você. Acho que pode ser algo interessante para o seu perfil, com potencial de crescimento e ótimos resultados! Podemos marcar uma conversa rápida para eu te explicar direitinho? Será ótimo compartilhar essa oportunidade com você."
    ),
    'convite_2': (
        "😊 Convite Amigável\n\n"
        "Oi [Nome do Convidado]! Como você está? Descobri uma oportunidade incrível que está me ajudando muito financeiramente, e logo lembrei de você. Acho que poderia te interessar! É algo flexível, que encaixa bem na rotina e dá pra fazer no seu ritmo. Que tal marcarmos um papo para eu te explicar melhor? 😊"
    ),
    'convite_3': (
        "🌍 Convite Flexível\n\n"
        "Oi [Nome do Convidado]! Tudo bem? Sei que você valoriza a liberdade de horário e a flexibilidade. Por isso, pensei em te falar sobre um projeto que estou desenvolvendo: super flexível e com possibilidade de trabalhar de qualquer lugar. Podemos marcar uma conversa rápida para te explicar tudo. É uma ótima chance de gerar renda e ter mais liberdade! O que acha?"
    ),
    'convite_4': (
        "💵 Convite Renda Extra\n\n"
        "Oi [Nome do Convidado], como estão as coisas? Já pensou em conseguir uma renda extra? Tenho uma oportunidade que pode encaixar bem com seu ritmo, super flexível. Podemos marcar uma conversa rápida? Assim te explico direitinho como funciona e você vê se faz sentido para você. 😊"
    ),
    'convite_5': (
        "🚀 Convite Empreendedor\n\n"
        "Oi [Nome do Convidado]! Lembrei de você e do seu perfil empreendedor. Como estão as coisas? Estou desenvolvendo um projeto que tem transformado a vida de muita gente e achei que você poderia gostar de conhecer. É uma oportunidade com grande potencial e suporte para empreender. Posso te explicar tudo em uma conversa rápida, assim te mostro todos os detalhes! Será ótimo compartilhar isso com você."
    ),
    'convite_6': (
        "👀 Convite Curioso\n\n"
        "Oi [Nome do Convidado]! Lembrei de você, tudo bem? Tô envolvido em um projeto novo e muito bacana, e achei que você poderia se interessar. 😊 Te explico melhor quando tivermos um tempinho para conversar. Acho que vai te surpreender! 😉"
    ),
    'convite_7': (
        "✨ Convite Inspirador\n\n"
        "Oi [Nome do Convidado]! Como você está? Estou trabalhando em um projeto que realmente mudou minha visão sobre alcançar meus sonhos e objetivos. É uma oportunidade que não só aumenta a renda, mas também oferece desenvolvimento pessoal e crescimento. Quer que eu te conte mais?"
    ),
    'convite_8': (
        "⏳ Convite para Pessoas Ocupadas\n\n"
        "Oi [Nome do Convidado]! Como estão as coisas? Entendo sua rotina! Eu também estava com a agenda bem cheia quando descobri uma forma de aumentar minha renda, mesmo com a agenda apertada. Acho que poderia te interessar! É uma oportunidade flexível, que você pode fazer no seu próprio ritmo e sem comprometer muito tempo. Podemos bater um papo rápido sobre?"
    ),
    'convite_9': (
        "📊 Convite para Quem Busca Estabilidade\n\n"
        "Oi [Nome do Convidado]! Tudo certo? Estou envolvido(a) em um projeto que oferece uma oportunidade de gerar uma renda extra de forma estável e segura. Acho que você poderia gostar! Podemos conversar rapidinho? Assim te conto tudo e você vê se se encaixa no que está buscando."
    ),
    'convite_10': (
        "🕒 Convite com Foco em Autonomia\n\n"
        "Oi [Nome do Convidado]! Como estão as coisas? Estou com uma oportunidade que oferece mais autonomia e liberdade para você decidir seu ritmo e seu horário. Pensei que poderia ser algo que você gostaria! Posso te explicar melhor em uma conversa rápida. É uma oportunidade de ter controle sobre sua renda e seu tempo. Que tal?"
    ),
    'convite_11': (
        "🧠 Convite Inovador\n\n"
        "Oi [Nome do Convidado]! Tenho explorado novas ideias e queria compartilhar com você um projeto que pode ser revolucionário. Estou buscando pessoas com visão e queiram inovar. Posso te contar mais?"
    ),
    'convite_12': (
        "🤝 Convite Networking\n\n"
        "Oi [Nome do Convidado]! Admiro sua habilidade de fazer conexões! Estou envolvido em um projeto com um grande potencial de networking, abrindo portas para novas oportunidades. Posso te mostrar como você pode usar sua rede para prosperar?"
    ),
    'convite_13': (
        "🌱 Convite para Crescimento\n\n"
        "Oi [Nome do Convidado]! Seu espírito de crescimento me inspira! Estou desenvolvendo um projeto que além de resultados financeiros oferece muito crescimento pessoal e profissional. Quer saber mais sobre essa jornada?"
    ),
    'convite_14': (
        "🎁 Convite Oportunidade\n\n"
        "Oi [Nome do Convidado]! Tenho uma oportunidade exclusiva que acho que você vai adorar! Estou abrindo as portas de um projeto que está transformando a vida de muitas pessoas. Que tal dar uma olhada de perto?"
    ),
    'convite_15': (
        "💡 Convite Solução\n\n"
        "Oi [Nome do Convidado]! Sabendo que você sempre está procurando soluções, tenho uma ideia que pode otimizar algo em sua vida!  Acredito que vai se encaixar com seus objetivos! Podemos marcar um horário para te explicar melhor?"
    )
}


@group_member_required
async def mostrar_convites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu com os modelos de convite."""
    keyboard = [
        [InlineKeyboardButton("📈 Profissional", callback_data="convite_1"), InlineKeyboardButton("😊 Amigável", callback_data="convite_2")],
        [InlineKeyboardButton("🌍 Flexível", callback_data="convite_3"), InlineKeyboardButton("💵 Renda Extra", callback_data="convite_4")],
        [InlineKeyboardButton("🚀 Empreendedor", callback_data="convite_5"), InlineKeyboardButton("👀 Curioso", callback_data="convite_6")],
        [InlineKeyboardButton("✨ Inspirador", callback_data="convite_7"), InlineKeyboardButton("⏳ P/ Ocupados", callback_data="convite_8")],
        [InlineKeyboardButton("📊 Estabilidade", callback_data="convite_9"), InlineKeyboardButton("🕒 Autonomia", callback_data="convite_10")],
        [InlineKeyboardButton("🧠 Inovador", callback_data="convite_11"), InlineKeyboardButton("🤝 Networking", callback_data="convite_12")],
        [InlineKeyboardButton("🌱 Crescimento", callback_data="convite_13"), InlineKeyboardButton("🎁 Oportunidade", callback_data="convite_14")],
        [InlineKeyboardButton("💡 Solução", callback_data="convite_15")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "Escolha um modelo de convite:"
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query and update.callback_query.message:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)


@group_member_required
async def enviar_convite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o texto do convite selecionado."""
    query = update.callback_query
    if not query or not query.data:
        logger.warning("enviar_convite chamado sem query ou data.")
        return
        
    await query.answer()

    if query.data in CONVITES_TEXT:
        keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="voltar_convites")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(CONVITES_TEXT[query.data], reply_markup=reply_markup)
    elif query.data == "voltar_convites":
        await mostrar_convites(update, context)

