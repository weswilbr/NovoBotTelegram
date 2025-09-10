# NOME DO ARQUIVO: features/community/channels.py
# REFACTOR: Gerencia a exibição de links para os canais da comunidade em diferentes plataformas.

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils.verification import group_member_required

# --- Dados dos Canais ---
# Os links foram movidos para este arquivo para torná-lo autossuficiente.
YOUTUBE_LINKS = [
    ("Dr José Benjamín Pérez Y Sara Meléndez", "https://www.youtube.com/@DrJos%C3%A9Benjam%C3%ADnP%C3%A9rezySaraM"),
    ("Weslley William", "https://www.youtube.com/@empreendedor-tf"),
    ("4Life Brasil", "https://www.youtube.com/channel/UCNXgsoT8RJtIKfcLkiEqkgg"),
    ("El Equipo de Triunfo", "https://www.youtube.com/@ElEquipoDeTriunfo"),
]

TELEGRAM_LINKS = [
    ("El Equipo de Triunfo (Oficial)", "https://t.me/+HVC9HbTU1DUwYzUx"),
    ("Dr José Benjamín Pérez Y Sara Meléndez", "https://t.me/+GuKV_KJhFJtkZjZh"),
    ("Bot Equipe Triunfo Brasil", "https://t.me/material4life"),
]

WHATSAPP_LINKS = [
    ("El Equipo de Triunfo", "https://whatsapp.com/channel/0029VapdVhL2UPB8yH6yS23L"),
]

# --- Handlers ---

@group_member_required
async def canais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu inicial com as opções de plataformas."""
    keyboard = [
        [InlineKeyboardButton("📺 YouTube", callback_data='youtube')],
        [InlineKeyboardButton("📲 Telegram", callback_data='telegram')],
        [InlineKeyboardButton("💬 WhatsApp", callback_data='whatsapp')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "Escolha a plataforma para ver os canais disponíveis:",
            reply_markup=reply_markup
        )

@group_member_required
async def handle_canais_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gerencia os cliques nos botões e exibe os canais correspondentes."""
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer()

    if query.data == 'youtube':
        buttons = [[InlineKeyboardButton(name, url=url)] for name, url in YOUTUBE_LINKS]
        buttons.append([InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_canais')])
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            text="📺 **Canais no YouTube**\n\nClique em um canal para abrir:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == 'telegram':
        buttons = [[InlineKeyboardButton(name, url=url)] for name, url in TELEGRAM_LINKS]
        buttons.append([InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_canais')])
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            text="📲 **Canais no Telegram**\n\nClique em um canal para abrir:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == 'whatsapp':
        buttons = [[InlineKeyboardButton(name, url=url)] for name, url in WHATSAPP_LINKS]
        buttons.append([InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_canais')])
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            text="💬 **Canais no WhatsApp**\n\nClique no canal para abrir:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == 'voltar_canais':
        keyboard = [
            [InlineKeyboardButton("📺 YouTube", callback_data='youtube')],
            [InlineKeyboardButton("📲 Telegram", callback_data='telegram')],
            [InlineKeyboardButton("💬 WhatsApp", callback_data='whatsapp')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Escolha a plataforma para ver os canais disponíveis:",
            reply_markup=reply_markup
        )

