# NOME DO ARQUIVO: features/user_tools/store_finder.py
# REFACTOR: Gerencia o ConversationHandler para o comando /minhaloja.
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, CommandHandler, ConversationHandler,
    MessageHandler, filters
)

# Estados da conversa
SOLICITAR_ID = 1

async def minha_loja(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia a conversa para obter o ID de Afiliado."""
    if not update.message: return ConversationHandler.END
    await update.message.reply_text("Para gerar o link da sua loja, por favor, informe seu ID de Afiliado:")
    return SOLICITAR_ID

async def capturar_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o ID, gera o link da loja e finaliza a conversa."""
    if not update.message: return ConversationHandler.END
    
    id_afiliado = update.message.text
    if not id_afiliado or not id_afiliado.isdigit():
        await update.message.reply_text("⚠️ ID inválido. Por favor, insira apenas números:")
        return SOLICITAR_ID

    url_da_loja = f"https://brazil.4life.com/{id_afiliado}"
    keyboard = [[InlineKeyboardButton("Visitar Loja 4LIFE 🛍️", url=url_da_loja)]]
    
    await update.message.reply_text(
        "✅ Link da sua loja gerado com sucesso! Clique no botão abaixo:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END

async def cancelar_conversa_loja(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a conversa de busca da loja."""
    if update.message:
        await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

# Handler da conversa
loja_handler = ConversationHandler(
    entry_points=[CommandHandler("minhaloja", minha_loja)],
    states={
        SOLICITAR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, capturar_id)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar_conversa_loja)],
)

