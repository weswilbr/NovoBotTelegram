# NOME DO ARQUIVO: features/community/rules.py
# REFACTOR: Define e exibe as regras do grupo.
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from utils.verification import group_member_required

logger = logging.getLogger(__name__)

# A constante com o texto das regras é definida aqui para manter o módulo autossuficiente.
TEXTO_REGRAS = (
    "📜 *Regras do Grupo de Compartilhamento de Materiais 4Life* 📜\n\n"
    "1. *Respeito*: Trate todos com gentileza.\n"
    "2. *Foco*: Compartilhe conteúdos relacionados à 4Life.\n"
    "3. *Evite Spam*: Mantenha o grupo organizado.\n"
    "4. *Privacidade*: Respeite a privacidade dos membros.\n"
    "5. *Conteúdo Apropriado*: Não compartilhe material ilegal.\n"
    "6. *Ajuda*: Sinta-se à vontade para apoiar outros membros.\n\n"
    "🙏 Obrigado por fazer parte da nossa comunidade! 🙌"
)

@group_member_required
async def mostrar_regras(update: Update, context: ContextTypes.DEFAULT_TYPE, edit_message: bool = False) -> bool:
    """
    Exibe as regras do grupo, editando a mensagem se solicitado.
    Retorna True se bem-sucedido, False caso contrário.
    """
    try:
        if edit_message and update.callback_query and update.callback_query.message:
            query = update.callback_query
            await query.edit_message_text(text=TEXTO_REGRAS, parse_mode='Markdown')
            return True
        elif update.effective_chat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=TEXTO_REGRAS, parse_mode='Markdown')
            return True
        return False
    except BadRequest as e:
        if "Message is not modified" in str(e):
            logger.warning("Mensagem de regras não modificada (já estava exibida).")
            return True  # Considera sucesso, pois a intenção foi atendida.
        else:
            logger.error(f"Erro de BadRequest ao exibir regras: {e}")
            return False
    except Exception as e:
        logger.error(f"Erro geral ao exibir regras: {e}", exc_info=True)
        return False

