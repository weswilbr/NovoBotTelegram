# NOME DO ARQUIVO: features/community/events.py
# REFACTOR: Handler para o comando /eventos, gerenciando a exibição de eventos.
import logging
from urllib.parse import quote
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import EVENTOS
from utils.verification import group_member_required

logger = logging.getLogger(__name__)

def gerar_link_google_calendar(evento):
    nome = evento['nome']
    data_hora = evento['data_hora']
    duracao = evento['duracao']
    start_time = data_hora.strftime("%Y%m%dT%H%M%SZ")
    end_time = (data_hora + duracao).strftime("%Y%m%dT%H%M%SZ")
    return f"https://www.google.com/calendar/render?action=TEMPLATE&text={quote(nome)}&dates={start_time}/{end_time}"

@group_member_required
async def escolher_local_evento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra os eventos disponíveis."""
    keyboard = [[evento["botao"]] for evento in EVENTOS.values() if evento.get("status") == "on"]
    if not keyboard:
        await update.message.reply_text("Nenhum evento programado no momento.")
        return
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌍 Escolha um evento para ver os detalhes:", reply_markup=reply_markup)

async def enviar_evento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia os detalhes de um evento selecionado."""
    query = update.callback_query
    evento_nome = query.data.split('_')[1]
    evento = EVENTOS.get(evento_nome)

    if not evento:
        await query.edit_message_text("⚠️ Evento não encontrado.")
        return

    google_calendar_url = gerar_link_google_calendar(evento)
    keyboard = [[InlineKeyboardButton("🗓️ Adicionar ao Google Calendar", url=google_calendar_url)]]
    
    await context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=evento["file_id_foto"],
        caption=evento["texto"]
    )
    if "file_id_video" in evento:
        await context.bot.send_video(chat_id=query.message.chat.id, video=evento["file_id_video"])

    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text="Adicione à sua agenda:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

