# NOME DO ARQUIVO: features/general/help.py
# REFACTOR: Contém o comando /ajuda, com o menu principal limpo e atualizado.

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Opcional: Se você usa este decorador e ele está funcionando, mantenha o import.
# Se não, remova-o junto com o @group_member_required abaixo.
from utils.verification import group_member_required

# A função 'start' foi removida deste arquivo para evitar duplicidade.
# A versão correta deve estar em 'features/general/start.py'.

@group_member_required
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o menu de ajuda completo e atualizado."""
    # Mensagem de ajuda sem os comandos removidos (/lista e /minhaloja)
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