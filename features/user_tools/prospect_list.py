# NOME DO ARQUIVO: features/user_tools/prospect_list.py
# REFACTOR: Gerencia a lógica completa para a lista de prospectos, incluindo ConversationHandlers e conexão com o banco de dados.

import os
import logging
import re
import psycopg2
from fpdf import FPDF
from urllib.parse import urlparse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from config import DATABASE_URL

logger = logging.getLogger(__name__)

# --- Estados da Conversa ---
NOME, TELEFONE, CIDADE = range(3)
EDITAR_NOME, EDITAR_TELEFONE, EDITAR_CIDADE = range(3, 6)

# --- Conexão com o Banco de Dados ---
def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL de forma robusta."""
    if not DATABASE_URL:
        logger.error("DATABASE_URL não está definida.")
        raise ValueError("A variável de ambiente DATABASE_URL não está definida.")
    try:
        result = urlparse(DATABASE_URL)
        return psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
            sslmode='require'
        )
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# CORREÇÃO 1: A função foi transformada em 'async def'
async def create_table_if_not_exists():
    """Cria a tabela de prospectos se ela não existir."""
    try:
        with get_db_connection() as conn:
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
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
        logger.error(f"Erro ao criar a tabela de prospectos: {e}")

# --- Funções Auxiliares ---
def is_private_chat(update: Update) -> bool:
    """Verifica se a interação ocorre em um chat privado."""
    return update.effective_chat is not None and update.effective_chat.type == 'private'

async def aviso_privacidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Informa o usuário que a funcionalidade deve ser usada no privado."""
    bot_username = (await context.bot.get_me()).username
    mensagem = (
        "🔒 *Sua privacidade é nossa prioridade!*\n\n"
        "Para gerenciar sua lista de prospectos, por favor, inicie uma "
        f"conversa privada comigo clicando aqui: @{bot_username}"
    )
    
    target_chat = update.effective_chat
    if target_chat:
        await target_chat.send_message(mensagem, parse_mode='Markdown')

# --- Handlers da Conversa de Adição ---
async def adicionar_prospecto_conversa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia a conversa para adicionar um novo prospecto."""
    if not is_private_chat(update):
        await aviso_privacidade(update, context)
        return ConversationHandler.END

    if update.message:
        await update.message.reply_text('📋 Vamos começar. Por favor, insira o *nome* do prospecto:', parse_mode='Markdown')
        return NOME
    return ConversationHandler.END

async def capturar_nome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o nome e solicita o telefone."""
    if update.message and update.message.text and context.user_data is not None:
        context.user_data['nome'] = update.message.text
        await update.message.reply_text('Agora, insira o *telefone*:', parse_mode='Markdown')
        return TELEFONE
    return ConversationHandler.END

async def capturar_telefone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o telefone e solicita a cidade."""
    if update.message and update.message.text and context.user_data is not None:
        context.user_data['telefone'] = update.message.text
        await update.message.reply_text('Para finalizar, insira a *cidade*:', parse_mode='Markdown')
        return CIDADE
    return ConversationHandler.END

async def capturar_cidade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura a cidade, confirma os dados e salva."""
    if not (update.message and update.message.text and context.user_data):
        return ConversationHandler.END

    context.user_data['cidade'] = update.message.text
    nome = context.user_data.get('nome', 'N/A')
    telefone = context.user_data.get('telefone', 'N/A')
    cidade = context.user_data.get('cidade', 'N/A')
    user_id = update.effective_user.id

    try:
        with get_db_connection() as conn:
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO prospectos (user_id, nome, telefone, cidade) VALUES (%s, %s, %s, %s)",
                        (user_id, nome, telefone, cidade)
                    )
                await update.message.reply_text(f"✅ Prospecto salvo com sucesso!\n\n👤 *Nome:* {nome}\n📞 *Telefone:* {telefone}\n🌆 *Cidade:* {cidade}", parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Erro ao salvar prospecto para user_id {user_id}: {e}")
        await update.message.reply_text("⚠️ Ocorreu um erro ao salvar os dados. Tente novamente mais tarde.")
    
    if context.user_data:
        context.user_data.clear()
    return ConversationHandler.END

async def cancelar_conversa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a conversa atual."""
    if context.user_data:
        context.user_data.clear()
    
    if update.message:
        await update.message.reply_text('❌ Operação cancelada.')
    elif update.callback_query:
        await update.callback_query.edit_message_text('❌ Operação cancelada.')

    return ConversationHandler.END

# --- Handlers de Gerenciamento (Listar, Remover, Editar) ---
async def listar_prospectos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista os prospectos do usuário com botões de ação."""
    if not is_private_chat(update) or not update.message:
        await aviso_privacidade(update, context)
        return
        
    user_id = update.effective_user.id
    try:
        with get_db_connection() as conn:
            if not conn:
                await update.message.reply_text("⚠️ Erro de conexão com o banco de dados.")
                return
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, nome FROM prospectos WHERE user_id = %s', (user_id,))
                rows = cursor.fetchall()

        if rows:
            keyboard = []
            for (prospecto_id, nome) in rows:
                keyboard.append([
                    InlineKeyboardButton(f"✏️ Editar {nome}", callback_data=f"editar_{prospecto_id}"),
                    InlineKeyboardButton(f"❌ Remover {nome}", callback_data=f"remover_{prospecto_id}")
                ])
            await update.message.reply_text("Selecione um prospecto para gerenciar:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_text("⚠️ Você ainda não adicionou prospectos. Use o comando `/prospectos_add` para começar.")
    except Exception as e:
        logger.error(f"Erro ao listar prospectos para user_id {user_id}: {e}")
        await update.message.reply_text("⚠️ Ocorreu um erro ao buscar sua lista.")

async def remover_prospecto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove um prospecto do banco de dados."""
    query = update.callback_query
    if not (query and query.data): return
    
    await query.answer()
    prospecto_id = query.data.split('_')[1]
    
    try:
        with get_db_connection() as conn:
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM prospectos WHERE id = %s AND user_id = %s', (prospecto_id, query.from_user.id))
        await query.edit_message_text("✅ Prospecto removido com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao remover prospecto ID {prospecto_id}: {e}")
        await query.edit_message_text("⚠️ Erro ao remover prospecto.")

async def editar_prospecto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Esta função agora é um placeholder, pois a lógica de edição foi movida para o ConversationHandler no main.py
    # para evitar complexidade de roteamento aqui. O callback_router irá ignorar este handler.
    pass

# --- Handlers de Relatórios ---
async def gerar_relatorio_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia um relatório em texto dos prospectos."""
    if not is_private_chat(update) or not update.message:
        await aviso_privacidade(update, context)
        return
        
    user_id = update.effective_user.id
    try:
        with get_db_connection() as conn:
            if not conn:
                await update.message.reply_text("⚠️ Erro de conexão com o banco de dados.")
                return
            with conn.cursor() as cursor:
                cursor.execute('SELECT nome, telefone, cidade FROM prospectos WHERE user_id = %s', (user_id,))
                rows = cursor.fetchall()
        
        if rows:
            relatorio = "📋 *Sua Lista de Prospectos:*\n\n"
            for idx, (nome, telefone, cidade) in enumerate(rows, 1):
                relatorio += f"*{idx}.*\n👤 *Nome:* {nome}\n📞 *Telefone:* {telefone}\n🌆 *Cidade:* {cidade}\n\n"
            await update.message.reply_text(relatorio, parse_mode='Markdown')
        else:
            await update.message.reply_text("⚠️ Você ainda não tem prospectos.")
    except Exception as e:
        logger.error(f"Erro ao gerar relatório para user_id {user_id}: {e}")
        await update.message.reply_text("⚠️ Erro ao gerar o relatório.")

async def enviar_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera e envia um PDF com a lista de prospectos."""
    if not is_private_chat(update) or not update.message:
        await aviso_privacidade(update, context)
        return
        
    user_id = update.effective_user.id
    try:
        with get_db_connection() as conn:
            if not conn:
                await update.message.reply_text("⚠️ Erro de conexão com o banco de dados.")
                return
            with conn.cursor() as cursor:
                cursor.execute('SELECT nome, telefone, cidade FROM prospectos WHERE user_id = %s', (user_id,))
                rows = cursor.fetchall()
        
        if not rows:
            await update.message.reply_text("⚠️ Você não tem prospectos para exportar.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Lista de Prospectos", 0, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 10, 'Nome', 1)
        pdf.cell(60, 10, 'Telefone', 1)
        pdf.cell(70, 10, 'Cidade', 1)
        pdf.ln()

        pdf.set_font("Arial", '', 12)
        for nome, telefone, cidade in rows:
            pdf.cell(60, 10, nome.encode('latin-1', 'replace').decode('latin-1'), 1)
            pdf.cell(60, 10, telefone.encode('latin-1', 'replace').decode('latin-1'), 1)
            pdf.cell(70, 10, cidade.encode('latin-1', 'replace').decode('latin-1'), 1)
            pdf.ln()
            
        file_path = f"/tmp/prospectos_{user_id}.pdf"
        pdf.output(file_path)

        await update.message.reply_document(open(file_path, 'rb'), filename=f"prospectos.pdf")
        os.remove(file_path)

    except Exception as e:
        logger.error(f"Erro ao gerar PDF para user_id {user_id}: {e}")
        await update.message.reply_text("⚠️ Erro ao gerar o arquivo PDF.")
        
# --- Handlers da Conversa de Edição (definidos aqui, mas usados no ConversationHandler em main.py) ---
async def capturar_nome_edicao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o novo nome durante a edição."""
    if update.message and update.message.text and context.user_data:
        context.user_data['nome'] = update.message.text
        await update.message.reply_text("Insira o novo *telefone*:", parse_mode='Markdown')
        return EDITAR_TELEFONE
    return ConversationHandler.END

async def capturar_telefone_edicao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura o novo telefone durante a edição."""
    if update.message and update.message.text and context.user_data:
        context.user_data['telefone'] = update.message.text
        await update.message.reply_text("Insira a nova *cidade*:", parse_mode='Markdown')
        return EDITAR_CIDADE
    return ConversationHandler.END

async def capturar_cidade_edicao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Captura a nova cidade e atualiza o banco."""
    if not (update.message and update.message.text and context.user_data):
        return ConversationHandler.END
        
    context.user_data['cidade'] = update.message.text
    prospecto_id = context.user_data.get('prospecto_id')
    nome = context.user_data.get('nome')
    telefone = context.user_data.get('telefone')
    cidade = context.user_data.get('cidade')
    user_id = update.effective_user.id
    
    try:
        with get_db_connection() as conn:
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE prospectos SET nome = %s, telefone = %s, cidade = %s WHERE id = %s AND user_id = %s",
                        (nome, telefone, cidade, prospecto_id, user_id)
                    )
        await update.message.reply_text("✅ Prospecto atualizado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao atualizar prospecto ID {prospecto_id}: {e}")
        await update.message.reply_text("⚠️ Erro ao atualizar os dados.")
        
    if context.user_data:
        context.user_data.clear()
    return ConversationHandler.END

# CORREÇÃO 2: A chamada desnecessária no final do arquivo foi REMOVIDA.
# A inicialização agora acontece apenas dentro da função main() em main.py.