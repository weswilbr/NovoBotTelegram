# NOME DO ARQUIVO: features/admin/commands.py
# REFACTOR: Contém todos os comandos restritos para administração do grupo.

import logging
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest, TelegramError
from functools import wraps
import re
from datetime import datetime, timedelta

from config import CANAL_ID_2, ADMIN_USER_IDS

logger = logging.getLogger(__name__)

# --- Decorators de Verificação ---

def admin_required(func):
    """
    Decorator que verifica se o usuário que executa o comando está na lista de administradores globais do bot.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        # Verifica se o ID do usuário está na lista de admins definida no config.py
        if not user or user.id not in ADMIN_USER_IDS:
            await update.message.reply_text("🚫 Acesso negado. Apenas administradores do bot podem usar este comando.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def group_command(func):
    """
    Decorator que verifica se o comando está sendo usado dentro de um grupo ou supergrupo.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.message.chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("Este comando só pode ser usado dentro de um grupo.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

# --- Funções Auxiliares ---

def _parse_time(time_str: str) -> timedelta | None:
    """Converte uma string de tempo (ex: 10m, 1h, 2d) para um objeto timedelta."""
    match = re.match(r"(\d+)([mhd])$", time_str.lower())
    if not match:
        return None
    
    value, unit = int(match.group(1)), match.group(2)
    if unit == 'm':
        return timedelta(minutes=value)
    if unit == 'h':
        return timedelta(hours=value)
    if unit == 'd':
        return timedelta(days=value)
    return None

# --- Comandos de Administração ---

@admin_required
@group_command
async def listar_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lista os administradores do chat atual."""
    chat_id = update.message.chat_id
    try:
        admins = await context.bot.get_chat_administrators(chat_id)
        if not admins:
            await update.message.reply_text("Não foi possível encontrar administradores neste chat.")
            return

        message = "👑 *Administradores deste Grupo:*\n"
        message += "\n".join(
            f"- {admin.user.mention_html()}" for admin in admins
        )
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    except (BadRequest, TelegramError) as e:
        logger.error(f"Erro ao listar admins: {e}")
        await update.message.reply_text(f"⚠️ Ocorreu um erro: {e.message}")

@admin_required
@group_command
async def silenciar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Silencia um membro. Uso: responda a uma mensagem com /silenciar [tempo] (ex: /silenciar 10m)."""
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Uso: Responda à mensagem do usuário que deseja silenciar.")
        return

    user_to_mute = update.message.reply_to_message.from_user
    chat_id = update.message.chat_id
    duration = timedelta(hours=1) # Duração padrão de 1 hora
    
    if context.args:
        parsed_duration = _parse_time(context.args[0])
        if parsed_duration:
            duration = parsed_duration
        else:
            await update.message.reply_text("Formato de tempo inválido. Use 'm' para minutos, 'h' para horas, 'd' para dias (ex: 30m, 2h, 1d).")
            return

    until_date = datetime.now() + duration
    
    try:
        await context.bot.restrict_chat_member(
            chat_id,
            user_to_mute.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await update.message.reply_text(f"🔇 O usuário {user_to_mute.mention_html()} foi silenciado por {str(duration).replace('0:', '', 1)}.", parse_mode=ParseMode.HTML)
    except (BadRequest, TelegramError) as e:
        await update.message.reply_text(f"⚠️ Erro ao silenciar: {e.message}")

@admin_required
@group_command
async def banir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bane um membro. Uso: responda a uma mensagem com /banir [motivo]."""
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Uso: Responda à mensagem do usuário que deseja banir.")
        return

    user_to_ban = update.message.reply_to_message.from_user
    chat_id = update.message.chat_id
    reason = " ".join(context.args) if context.args else "Nenhum motivo fornecido."

    try:
        await context.bot.ban_chat_member(chat_id, user_to_ban.id)
        await update.message.reply_text(f"🔨 O usuário {user_to_ban.mention_html()} foi banido.\n*Motivo:* {reason}", parse_mode=ParseMode.HTML)
    except (BadRequest, TelegramError) as e:
        await update.message.reply_text(f"⚠️ Erro ao banir: {e.message}")

@admin_required
@group_command
async def desbanir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove o banimento de um membro. Uso: /desbanir <user_id>."""
    if not context.args:
        await update.message.reply_text("⚠️ Uso: /desbanir <ID do usuário>")
        return
    
    try:
        user_id = int(context.args[0])
        chat_id = update.message.chat_id
        await context.bot.unban_chat_member(chat_id, user_id)
        await update.message.reply_text(f"✅ O usuário com ID {user_id} foi desbanido.")
    except (ValueError, IndexError):
        await update.message.reply_text("ID de usuário inválido. Por favor, forneça um número.")
    except (BadRequest, TelegramError) as e:
        await update.message.reply_text(f"⚠️ Erro ao desbanir: {e.message}")

@admin_required
@group_command
async def fixar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fixa uma mensagem no grupo. Uso: responda à mensagem que deseja fixar."""
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Uso: Responda à mensagem que deseja fixar.")
        return

    try:
        await context.bot.pin_chat_message(
            chat_id=update.message.chat_id,
            message_id=update.message.reply_to_message.message_id,
            disable_notification=True
        )
        await update.message.reply_text("📌 Mensagem fixada!")
    except (BadRequest, TelegramError) as e:
        await update.message.reply_text(f"⚠️ Erro ao fixar: {e.message}")

@admin_required
@group_command
async def desfixar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Desafixa a mensagem mais recente fixada no grupo."""
    try:
        await context.bot.unpin_chat_message(chat_id=update.message.chat_id)
        await update.message.reply_text("📌 Mensagem desafixada!")
    except (BadRequest, TelegramError) as e:
        await update.message.reply_text(f"⚠️ Erro ao desafixar: {e.message}")

@admin_required
async def enviartextocanal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de texto para o canal configurado. Suporta Markdown."""
    if not context.args:
        await update.message.reply_text("⚠️ Uso: /enviartextocanal <mensagem>")
        return
    
    try:
        mensagem = " ".join(context.args)
        await context.bot.send_message(
            chat_id=CANAL_ID_2,
            text=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )
        await update.message.reply_text("✅ Mensagem enviada para o canal com sucesso!")
    except BadRequest as e:
        if "can't parse entities" in e.message:
            await update.message.reply_text("⚠️ Erro de formatação. Verifique sua sintaxe Markdown (ex: `*texto*`, `_texto_`).")
        else:
            await update.message.reply_text(f"⚠️ Erro ao enviar: {e.message}")
    except TelegramError as e:
        logger.error(f"Erro ao enviar mensagem para o canal {CANAL_ID_2}: {e}")
        await update.message.reply_text(f"⚠️ Erro ao enviar: {e.message}")