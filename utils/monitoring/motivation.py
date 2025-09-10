# NOME DO ARQUIVO: utils/monitoring/motivation.py
# REFACTOR: Lógica para selecionar e enviar mensagens motivacionais agendadas.
import random
import logging
from telegram.ext import CallbackContext
from features.products.data import FRASES_MOTIVACIONAIS

logger = logging.getLogger(__name__)

frases_enviadas_recentemente = []
MAX_RECENTES = min(10, len(FRASES_MOTIVACIONAIS) // 2)

def escolher_frase():
    """Escolhe uma frase que não foi enviada recentemente."""
    frase_escolhida = random.choice(FRASES_MOTIVACIONAIS)
    tentativas = 0
    while frase_escolhida in frases_enviadas_recentemente and tentativas < 5:
        frase_escolhida = random.choice(FRASES_MOTIVACIONAIS)
        tentativas += 1
    
    frases_enviadas_recentemente.append(frase_escolhida)
    if len(frases_enviadas_recentemente) > MAX_RECENTES:
        frases_enviadas_recentemente.pop(0)
    return frase_escolhida

async def enviar_motivacao(context: CallbackContext) -> None:
    """Envia uma frase motivacional para o chat_id configurado no job."""
    try:
        chat_id = context.job.data
        if not chat_id: return

        frase = escolher_frase()
        introducoes = ["Lembrete do dia:", "Para inspirar sua jornada:", "Uma dose de motivação:"]
        mensagem = f"*{random.choice(introducoes)}*\n\n{frase} ✨"
        
        await context.bot.send_message(chat_id=chat_id, text=mensagem, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Erro ao enviar frase motivacional: {e}")

