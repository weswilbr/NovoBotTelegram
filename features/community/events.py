# NOME DO ARQUIVO: features/community/events.py
# REFACTOR: Gerencia a exibição de eventos e a criação de links para o Google Calendar.

import logging
from datetime import datetime, timedelta
from urllib.parse import quote
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# Os dados dos eventos foram movidos para este arquivo para torná-lo autossuficiente.
EVENTOS = {
    "Boa Vista 🇧🇷": {
        "file_id_foto": "AgACAgEAAxkBAAImKGcou0nzeJOY5mCvomwaLphxCV_nAAJJrTEbrGlARajSxbtHP1ucAQADAgADeQADNgQ",
        "texto": (
            "Você já se perguntou alguma vez como seria sua vida desfrutando de total liberdade de tempo e ao mesmo tempo gerando renda?\n\n"
            "Você já teve necessidade de ter 2 ou até 3 empregos porque o dinheiro não basta? 🥴 Você está procurando uma renda extra ou algo que lhe dê mais tempo para você e sua família? Se sim, esta oportunidade é para você.🤗\n\n"
            "➡️ Convidamos você a ouvir essa grande oportunidade de negócio. Sem a necessidade de ter nível acadêmico ou ser profissional. Está ao alcance de todos e é também um projeto com alcance global 🌎. 🤩\n\n"
            "Separe seu espaço na sua agenda.🗓️\n"
            "✨ *Reunião presencial nesta*\n"
            "Quarta-feira👩🏼‍💻\n"
            "Data: 06/11/2025.\n"
            "Horário: 20 horas.\n"
            "Local: Avenida Capitão Ene Garcez, 427. Centro. Boa Vista, Roraima.\n\n"
            "📸 Estamos esperando por você! 🤗"
        ),
        "data_hora": datetime(2025, 11, 6, 20, 0),
        "duracao": timedelta(hours=1),
        "status": "on", # "on" para ativo, "off" para desativado
    },
    "Reunião Central Brasil - Online": {
        "file_id_foto": "BQACAgEAAxkBAAIzZmdF6ntI9WJwkFJi6WD4X0oI_JpaAAImBAAC_9UxRsstOs1Mug4fNgQ",
        "file_id_video": "BAACAgEAAxkBAAIzaGdF6zJj9SZQKzm2hYxarqRYJNoCAAInBAAC_9UxRizlsRA8gE2sNgQ",
        "texto": (
            "Você já se perguntou alguma vez como seria sua vida desfrutando de total liberdade de tempo e ao mesmo tempo gerando renda?\n\n"
            "Você já teve necessidade de ter 2 ou até 3 empregos porque o dinheiro não basta? 🥴 Você está procurando uma renda extra ou algo que lhe dê mais tempo para você e sua família? Se sim, esta oportunidade é para você.🤗\n\n"
            "➡️ Convidamos você a ouvir essa grande oportunidade de negócio. Sem a necessidade de ter nível acadêmico ou ser profissional. Está ao alcance de todos e é também um projeto com alcance global 🌎. 🤩\n\n"
            "Separe seu espaço na sua agenda.🗓️\n"
            "✨ Reunião virtual pelo zoom 👩🏼‍💻\n"
            "Data: terça-feira, 26 de novembro de 2025 às 20:00 horário de Brasília\n\n"
            "Basta clicar no link para acessar 🤩👇🏻\n\n"
            "📲 Link para reunião via Zoom\n"
            "https://us02web.zoom.us/j/88066207020?pwd=S0tKUEdYMkNiUmNydkJrM3dsMEhwQT09b\n\n"
            "📸 Estamos esperando por você! 🤗"
        ),
        "data_hora": datetime(2025, 11, 26, 20, 0),
        "duracao": timedelta(hours=1),
        "status": "on", # "on" para ativo, "off" para desativado
    }
}

def gerar_link_google_calendar(evento_nome: str, data_hora: datetime, duracao: timedelta, location: str) -> str:
    """Gera um link do Google Calendar para o evento."""
    start_time_str = data_hora.strftime("%Y%m%dT%H%M%SZ")
    end_time_str = (data_hora + duracao).strftime("%Y%m%dT%H%M%SZ")
    google_calendar_url = (
        f"https://www.google.com/calendar/render?action=TEMPLATE&text={quote(evento_nome)}&"
        f"dates={start_time_str}/{end_time_str}&"
        f"details=Participe+da+reunião.&"
        f"location={quote(location)}"
    )
    return google_calendar_url

@group_member_required
async def escolher_local_evento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia o menu inicial para escolha do evento."""
    keyboard = [
        [InlineKeyboardButton(nome, callback_data=f"evento_{nome}")]
        for nome, detalhes in EVENTOS.items() if detalhes.get("status") == "on"
    ]
    if not keyboard:
        await update.message.reply_text("Nenhum evento programado no momento. Fique atento para mais informações em breve!")
        return

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌍 Escolha um evento para ver mais detalhes:",
        reply_markup=reply_markup
    )

@group_member_required
async def enviar_evento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com o callback do botão e envia os detalhes do evento."""
    query = update.callback_query
    if not (query and query.data): return
    
    await query.answer()
    
    evento_nome = query.data.replace("evento_", "")
    evento = EVENTOS.get(evento_nome)

    if not evento:
        await query.message.reply_text("⚠️ Evento não encontrado ou não está mais ativo.")
        return

    # Extrai o local do texto do evento para o link do calendário
    location_info = "Online via Zoom"
    if "Local:" in evento["texto"]:
        location_info = evento["texto"].split("Local:")[1].split("\n\n")[0].strip()

    google_calendar_url = gerar_link_google_calendar(evento_nome, evento["data_hora"], evento["duracao"], location_info)

    try:
        if evento.get("file_id_foto"):
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=evento["file_id_foto"],
                caption=evento["texto"]
            )

        if evento.get("file_id_video"):
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=evento["file_id_video"]
            )

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗓️ Adicionar ao Google Calendar", url=google_calendar_url)]]
        )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Adicione o evento à sua agenda:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Erro ao enviar detalhes do evento '{evento_nome}': {e}")
        await query.message.reply_text("⚠️ Ocorreu um erro ao buscar os detalhes do evento.")

