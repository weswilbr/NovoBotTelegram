# NOME DO ARQUIVO: utils/monitoring/motivation.py
# REFACTOR: Gerencia a seleção e o envio de mensagens motivacionais agendadas.

import random
import logging
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

# Lista de frases motivacionais com emojis.
# Definida localmente para tornar o módulo autossuficiente.
FRASES_MOTIVACIONAIS = [
    "🌟 Confie na sua jornada! Cada grande transformação se inicia com o primeiro passo. Dê o seu hoje!",
    "💪 Sucesso é a soma de esforço focado, determinação inabalável e persistência diária. Continue construindo o seu!",
    "🚀 A chave para desbloquear seu potencial? Nunca desista dos seus sonhos! A persistência te levará longe.",
    "🧗 Encare cada desafio como um degrau para o seu crescimento. Supere-o e fique mais forte!",
    "🌈 Mire nas estrelas, dedique-se com paixão e mantenha viva a chama da sua crença. Você pode!",
    "📉 Tropeçou? Ótimo! Cada falha é um aprendizado valioso no seu caminho rumo ao sucesso. Levante e siga!",
    "🎯 Olhos no prêmio! Mantenha o foco, confie no seu imenso potencial e avance com convicção.",
    "🌱 Plante suas melhores ações hoje. A colheita de amanhã será reflexo da sua dedicação agora!",
    "🔥 Acenda a chama da ação hoje! Seu 'eu' do futuro vai te agradecer imensamente por cada esforço.",
    "🏗️ A persistência constrói pontes onde antes só havia abismos. Não pare!",
]

frases_enviadas_recentemente = []
MAX_RECENTES = min(5, len(FRASES_MOTIVACIONAIS) // 2)

def escolher_frase():
    """Escolhe uma frase que não tenha sido enviada recentemente."""
    if len(frases_enviadas_recentemente) >= len(FRASES_MOTIVACIONAIS):
        frases_enviadas_recentemente.clear()

    frase_escolhida = random.choice(FRASES_MOTIVACIONAIS)
    tentativas = 0
    while frase_escolhida in frases_enviadas_recentemente and tentativas < 10:
        frase_escolhida = random.choice(FRASES_MOTIVACIONAIS)
        tentativas += 1
    
    frases_enviadas_recentemente.append(frase_escolhida)
    if len(frases_enviadas_recentemente) > MAX_RECENTES:
        frases_enviadas_recentemente.pop(0)
    
    return frase_escolhida

async def enviar_motivacao_agendada(context: CallbackContext) -> None:
    """Função de job para enviar uma frase motivacional a um chat_id específico."""
    if not context.job or not context.job.chat_id:
        logger.warning("Job de motivação executado sem chat_id.")
        return

    chat_id = context.job.chat_id
    frase = escolher_frase()
    
    introducoes = [
        "Lembrete do dia:", "Para inspirar sua jornada:", "Uma dose de motivação para você:",
        "Acredite e vá:", "Pensamento do momento:", "Para você refletir e agir:"
    ]
    mensagem = f"*{random.choice(introducoes)}*\n\n{frase} ✨"
    
    try:
        await context.bot.send_message(chat_id=chat_id, text=mensagem, parse_mode='Markdown')
        logger.info(f"Frase motivacional agendada enviada para o chat_id {chat_id}")
    except Exception as e:
        logger.error(f"Erro ao enviar frase motivacional agendada para o chat_id {chat_id}: {e}")

