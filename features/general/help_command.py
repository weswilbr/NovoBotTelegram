# NOME DO ARQUIVO: features/general/help_command.py
# REFACTOR: Centraliza os comandos /start e /ajuda com menu completo e decorador funcional.

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ParseMode

# Importa o decorador REAL que acabamos de criar
from utils.decorators import group_member_required

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    user_name = update.effective_user.first_name
    if update.message.chat.type == ChatType.PRIVATE:
        text = (
            f"👋 Olá, *{user_name}*! Eu sou seu Assistente Virtual.\n\n"
            "Para explorar todas as minhas funcionalidades, por favor, me adicione ao "
            "nosso grupo principal e digite /ajuda por lá!"
        )
    else:
        text = f"👋 Olá, *{user_name}*! Para ver a lista completa de comandos, digite /ajuda."
    
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

@group_member_required  # <-- Agora este decorador tem uma função real!
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de ajuda completo e atualizado."""
    # Mensagem de ajuda completa, refletindo os comandos reais do bot
    mensagem_ajuda = (
        "🌟 *Menu de Ajuda do Bot* 🌟\n\n"
        "Explore as diversas funcionalidades do bot!\n\n"
        "🚀 *Negócios & Treinamentos:*\n"
        "   • /marketingrede - Saiba mais sobre Marketing de Rede\n"
        "   • /recompensas2024 - Conheça o Plano de Recompensas 2024\n"
        "   • /bonusconstrutor - Entenda o Bônus Construtor\n\n"
        "💰 *Produtos & Benefícios:*\n"
        "   • /glossario - Consulte termos e conceitos\n"
        "   • /tabelas - Consulte as tabelas de preços e pontos\n"
        "   • /produtos - Descubra os benefícios dos produtos\n"
        "   • /fabrica4life - Conheça a fábrica 4LIFE\n"
        "   • /fatorestransferencia - Saiba sobre os Fatores de Transferência\n"
        "   • /fidelidade - Informações sobre o programa de fidelidade\n\n"
        "📣 *Materiais e Comunidade:*\n"
        "   • /folheteria - Acesse panfletos e o catálogo\n"
        "   • /eventos - Veja os próximos eventos\n"
        "   • /convite - Envie modelos de convites\n"
        "   • /regras - Veja as regras do grupo\n\n"
        "⚙️ *Comandos Gerais:*\n"
        "   • /start - Inicia uma conversa com o bot\n"
        "   • /ajuda - Exibe esta mensagem de ajuda\n"
    )

    # Lógica para responder a um botão (callback) ou a uma mensagem
    if update.callback_query:
        await update.callback_query.edit_message_text(mensagem_ajuda, parse_mode='Markdown')
    else:
        await update.message.reply_text(mensagem_ajuda, parse_mode='Markdown')