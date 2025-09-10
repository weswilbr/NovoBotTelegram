# NOME DO ARQUIVO: features/creative/art_creator.py
# REFACTOR: Handler para o comando /artes e a lógica de interação do menu de criativos.
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from .art_data import MEDIA_CONTENT

logger = logging.getLogger(__name__)

async def artes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu principal de criação de artes."""
    keyboard = [
        [InlineKeyboardButton("👕 Logo 4Life (Camisetas)", callback_data="arte_camiseta")],
        [InlineKeyboardButton("🎉 Banner de Produtos", callback_data="banner_produtos")],
        [InlineKeyboardButton("💡 Criativos (Modelos)", callback_data="menu_criativos")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🎨 Olá {update.effective_user.first_name}, escolha uma opção de arte:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com todos os callbacks do módulo de artes."""
    query = update.callback_query
    await query.answer()

    user_first_name = query.from_user.first_name
    chat_id = query.message.chat.id
    action = query.data

    if action == "arte_camiseta":
        content_info = MEDIA_CONTENT['artes_fixas'].get('arte_camiseta')
        if content_info:
            caption = content_info['caption_template'].format(user_first_name=user_first_name)
            await context.bot.send_document(chat_id=chat_id, document=content_info['file_id'], caption=caption)

    elif action == "banner_produtos":
        await query.message.reply_text("Enviando banners...")
        for key in ['bannerprodutos', 'bannerprodutos1']:
             content_info = MEDIA_CONTENT['artes_fixas'].get(key)
             if content_info:
                 await context.bot.send_document(chat_id=chat_id, document=content_info['file_id'])

    elif action == "menu_criativos":
        keyboard = [
            [InlineKeyboardButton("🖼️ Imagem Estática", callback_data="criativo_imagem_estatica")],
            [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar_menu_artes_principal")]
        ]
        await query.edit_message_text("💡 Escolha um tipo:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action.startswith("criativo_"):
        await query.edit_message_text(
            text=f"Modelos de {action.split('_')[1].title()} em breve.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Voltar", callback_data="menu_criativos")]])
        )

    elif action == "voltar_menu_artes_principal":
         await artes(update, context) # Simplificado para chamar a função principal novamente

