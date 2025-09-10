# NOME DO ARQUIVO: features/user_tools/prospect_list.py
# REFACTOR: Gerencia a lista de prospectos do usuário (comandos, ConversationHandler e interações com DB).
import os
import psycopg2
import logging
from fpdf import FPDF
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from config import DATABASE_URL

logger = logging.getLogger(__name__)

# Estados da conversa
NOME, TELEFONE, CIDADE = range(3)
EDITAR_NOME, EDITAR_TELEFONE, EDITAR_CIDADE = range(3, 6)

def get_db_connection():
    """Obtém a conexão com o banco de dados a partir da URL de configuração."""
    if not DATABASE_URL:
        raise ConnectionError("DATABASE_URL não está configurada.")
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def create_table_if_not_exists():
    """Cria a tabela de prospectos se ela não existir."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS prospectos (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        nome TEXT,
                        telefone TEXT,
                        cidade TEXT
                    );
                """)
        logger.info("Tabela 'prospectos' verificada/criada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao criar a tabela de prospectos: {e}", exc_info=True)

# Garante que a tabela exista quando o módulo for carregado
create_table_if_not_exists()

# --- Funções do ConversationHandler ---

async def adicionar_prospecto_conversa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia a conversa para adicionar um novo prospecto."""
    if not (update.message and update.message.chat and context.bot):
        return ConversationHandler.END
        
    if update.message.chat.type != 'private':
        bot_username = (await context.bot.get_me()).username
        await update.message.reply_text(
            f"🔒 Para sua privacidade, esta função só pode ser usada em uma [conversa privada](t.me/{bot_username}).",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    await update.message.reply_text('📋 Insira o *nome* do prospecto:', parse_mode='Markdown')
    return NOME

async def capturar_nome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o nome e solicita o telefone."""
    if not (update.message and update.message.text and context.user_data):
        logger.warning("capturar_nome: update.message, text ou context.user_data está faltando.")
        return ConversationHandler.END
        
    context.user_data['nome'] = update.message.text
    await update.message.reply_text('📞 Agora, insira o *telefone*:', parse_mode='Markdown')
    return TELEFONE

async def capturar_telefone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o telefone e solicita a cidade."""
    if not (update.message and update.message.text and context.user_data):
        logger.warning("capturar_telefone: update.message, text ou context.user_data está faltando.")
        return ConversationHandler.END
        
    context.user_data['telefone'] = update.message.text
    await update.message.reply_text('🌆 Por último, a *cidade*:', parse_mode='Markdown')
    return CIDADE

async def capturar_cidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Finaliza a coleta de dados e pede confirmação."""
    if not (update.message and update.message.text and context.user_data):
        logger.warning("capturar_cidade: update.message, text ou context.user_data está faltando.")
        return ConversationHandler.END
        
    context.user_data['cidade'] = update.message.text
    nome = context.user_data.get('nome', 'N/A')
    telefone = context.user_data.get('telefone', 'N/A')
    cidade = context.user_data.get('cidade', 'N/A')
    
    text = (f"📋 *Confirme os dados:*\n\n"
            f"👤 *Nome:* {nome}\n"
            f"📞 *Telefone:* {telefone}\n"
            f"🌆 *Cidade:* {cidade}\n\n"
            "Salvar estas informações?")
            
    keyboard = [[InlineKeyboardButton("✅ Confirmar", callback_data="confirmar_prospecto"), InlineKeyboardButton("❌ Cancelar", callback_data="cancelar_prospecto")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    return ConversationHandler.END

async def cancelar_conversa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a operação atual."""
    if context.user_data:
        context.user_data.clear()
        
    if update.callback_query and update.callback_query.message:
        await update.callback_query.edit_message_text('❌ Operação cancelada.')
    elif update.message:
        await update.message.reply_text('❌ Operação cancelada.')
    return ConversationHandler.END

# --- Funções de Callback e Comandos ---

async def confirmar_dados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Salva os dados do prospecto no banco de dados após confirmação."""
    query = update.callback_query
    if not (query and query.from_user and context.user_data and query.message):
        logger.error("confirmar_dados: query, from_user, message ou user_data está faltando.")
        if query: await query.answer("Erro interno.", show_alert=True)
        return

    await query.answer()
    user_id = query.from_user.id
    nome = context.user_data.get('nome')
    telefone = context.user_data.get('telefone')
    cidade = context.user_data.get('cidade')

    if not all([nome, telefone, cidade]):
        await query.edit_message_text("⚠️ Erro: dados incompletos. Tente novamente com /addprospecto.")
        return

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO prospectos (user_id, nome, telefone, cidade) VALUES (%s, %s, %s, %s)",
                            (user_id, nome, telefone, cidade))
        await query.edit_message_text(f"✅ Prospecto *{nome}* salvo com sucesso!", parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Erro ao salvar prospecto para user {user_id}: {e}")
        await query.edit_message_text("⚠️ Ocorreu um erro ao salvar. Tente novamente.")
    finally:
        if context.user_data:
            context.user_data.clear()

async def listar_prospectos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista os prospectos do usuário com botões de ação."""
    if not (update.message and update.message.from_user): return
    await update.message.reply_text("Função 'listar_prospectos' em desenvolvimento.")

async def gerar_relatorio_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera e envia um relatório em texto dos prospectos."""
    if not (update.message and update.message.from_user): return
    await update.message.reply_text("Função 'gerar_relatorio_comando' em desenvolvimento.")

async def enviar_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera e envia um relatório em PDF dos prospectos."""
    if not (update.message and update.message.from_user): return
    await update.message.reply_text("Função 'enviar_pdf' em desenvolvimento.")

async def remover_prospecto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove um prospecto da lista."""
    if not (update.callback_query and update.callback_query.message): return
    await update.callback_query.message.reply_text("Função 'remover_prospecto' em desenvolvimento.")

async def editar_prospecto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia a conversa para editar um prospecto existente."""
    if not (update.callback_query and update.callback_query.message): return ConversationHandler.END
    await update.callback_query.message.reply_text("Função 'editar_prospecto' em desenvolvimento.")
    return EDITAR_NOME
    
async def capturar_nome_edicao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o novo nome durante a edição."""
    if not (update.message and update.message.text): return ConversationHandler.END
    await update.message.reply_text("Função 'capturar_nome_edicao' em desenvolvimento.")
    return EDITAR_TELEFONE
    
async def capturar_telefone_edicao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o novo telefone durante a edição."""
    if not (update.message and update.message.text): return ConversationHandler.END
    await update.message.reply_text("Função 'capturar_telefone_edicao' em desenvolvimento.")
    return EDITAR_CIDADE
    
async def capturar_cidade_edicao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura a nova cidade e finaliza a edição."""
    if not (update.message and update.message.text): return ConversationHandler.END
    await update.message.reply_text("Função 'capturar_cidade_edicao' em desenvolvimento.")
    return ConversationHandler.END

