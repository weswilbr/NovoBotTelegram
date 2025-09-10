# NOME DO ARQUIVO: features/general/help.py
# REFACTOR: Contém os comandos /start e /ajuda, exibindo o menu principal de ajuda.
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ParseMode
from utils.verification import group_member_required

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    user_name = update.effective_user.first_name
    if update.message.chat.type == ChatType.PRIVATE:
        text = f"👋 Olá, *{user_name}*! Bem-vindo ao Assistente Virtual. Para ver todos os comandos, use /ajuda no nosso grupo principal."
    else:
        text = f"👋 Olá, *{user_name}*! Para ver a lista de comandos, digite /ajuda."
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

@group_member_required
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de ajuda completo."""
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
        "   • /fidelidade - Informações sobre o programa de fidelidade\n"
        "   • /minhaloja - Acesse sua loja personalizada\n\n"
        "📣 *Materiais e Comunidade:*\n"
        "   • /folheteria - Acesse panfletos e o catálogo\n"
        "   • /eventos - Veja os próximos eventos\n"
        "   • /convite - Envie modelos de convites\n"
        "   • /regras - Veja as regras do grupo\n\n"
        "🧰 *Ferramentas Pessoais:*\n"
        "   • /lista - Gerencie sua lista de prospectos (apenas no privado)\n\n"
        "⚙️ *Comandos Gerais:*\n"
        "   • /start - Inicia uma conversa com o bot\n"
        "   • /ajuda - Exibe esta mensagem de ajuda\n"
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(mensagem_ajuda, parse_mode='Markdown')
    else:
        await update.message.reply_text(mensagem_ajuda, parse_mode='Markdown')

