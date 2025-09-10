# NOME DO ARQUIVO: features/community/channels.py
# REFACTOR: Handler para o comando /canais, exibindo links para os canais da comunidade.
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from features.products.data import YOUTUBE_LINKS, TELEGRAM_LINKS, WHATSAPP_LINKS

async def canais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu inicial com as opções de plataformas."""
    keyboard = [
        [InlineKeyboardButton("📺 YouTube", callback_data='youtube')],
        [InlineKeyboardButton("📲 Telegram", callback_data='telegram')],
        [InlineKeyboardButton("💬 WhatsApp", callback_data='whatsapp')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Escolha a plataforma para ver os canais disponíveis:",
        reply_markup=reply_markup
    )

async def handle_canais_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gerencia os cliques nos botões e exibe os canais correspondentes."""
    query = update.callback_query
    platform = query.data

    links_map = {
        'youtube': ("📺 **Canais no YouTube**", YOUTUBE_LINKS),
        'telegram': ("📲 **Canais no Telegram**", TELEGRAM_LINKS),
        'whatsapp': ("💬 **Canais no WhatsApp**", WHATSAPP_LINKS),
    }

    if platform in links_map:
        title, links = links_map[platform]
        buttons = [[InlineKeyboardButton(name, url=url)] for name, url in links]
        buttons.append([InlineKeyboardButton("⬅️ Voltar", callback_data='voltar_canais')])
        await query.edit_message_text(
            text=f"{title}\n\nClique em um canal para abrir:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )
    elif platform == 'voltar_canais':
        keyboard = [
            [InlineKeyboardButton("📺 YouTube", callback_data='youtube')],
            [InlineKeyboardButton("📲 Telegram", callback_data='telegram')],
            [InlineKeyboardButton("💬 WhatsApp", callback_data='whatsapp')],
        ]
        await query.edit_message_text(
            text="Escolha a plataforma para ver os canais disponíveis:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

