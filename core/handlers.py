# NOME DO ARQUIVO: features/products/handlers.py
# REFACTOR: Gerencia o comando /produtos e todos os submenus e callbacks relacionados.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from utils.verification import group_member_required
from .data import MEDIA, PITCH_DE_VENDA_TEXT

logger = logging.getLogger(__name__)

# --- Funções de Geração de Menu (Dinâmicas) ---

def _get_main_menu() -> InlineKeyboardMarkup:
    """Cria o menu principal de categorias de produtos."""
    keyboard = [
        [InlineKeyboardButton("📦 Produtos Individuais", callback_data='products_submenu_individual')],
        # Adicione aqui outras categorias se necessário, seguindo o padrão
        # [InlineKeyboardButton("🏆 Top Pack", callback_data='products_show_toppack')],
    ]
    return InlineKeyboardMarkup(keyboard)

def _get_individual_products_submenu() -> InlineKeyboardMarkup:
    """Gera dinamicamente o submenu com todos os produtos individuais a partir do arquivo de dados."""
    buttons = []
    row = []
    # Itera sobre o dicionário de produtos para criar os botões
    for key, product_data in MEDIA.get('produtos', {}).items():
        label = product_data.get('label', key.capitalize())
        row.append(InlineKeyboardButton(label, callback_data=f'products_show_{key}'))
        # Agrupa os botões em linhas de 2 para melhor visualização
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton("🔙 Voltar ao Menu Principal", callback_data='products_main')])
    return InlineKeyboardMarkup(buttons)

def _get_product_options_menu(product_key: str) -> InlineKeyboardMarkup:
    """Gera o menu de opções (foto, vídeo, pitch) para um produto específico."""
    product_data = MEDIA.get('produtos', {}).get(product_key, {})
    buttons = []
    
    # Adiciona botões apenas se a mídia correspondente existir nos dados
    if product_data.get('foto'):
        buttons.append(InlineKeyboardButton("📷 Ver Foto", callback_data=f"products_send_{product_key}_foto"))
    if product_data.get('video'):
        buttons.append(InlineKeyboardButton("🎥 Ver Vídeo", callback_data=f"products_send_{product_key}_video"))
    if product_data.get('documento'):
        buttons.append(InlineKeyboardButton("📄 Ver Documento", callback_data=f"products_send_{product_key}_documento"))
    if PITCH_DE_VENDA_TEXT.get(product_key):
        buttons.append(InlineKeyboardButton("📝 Pitch de Venda", callback_data=f"products_pitch_{product_key}"))

    # Organiza os botões em um layout de duas colunas e adiciona o de "Voltar"
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Voltar para a Lista", callback_data='products_submenu_individual')])
    return InlineKeyboardMarkup(keyboard)


# --- Funções de Lógica e Handlers ---

@group_member_required
async def beneficiosprodutos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler do comando /produtos. Exibe ou edita para o menu principal de produtos."""
    text = "🛍️ *Menu de Produtos*\n\nSelecione uma categoria para ver os materiais disponíveis:"
    reply_markup = _get_main_menu()
    
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        elif update.message:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except TelegramError as e:
        logger.error(f"Erro ao mostrar menu de produtos: {e}")


async def _show_individual_products_submenu(query: Update.callback_query) -> None:
    """Edita a mensagem para mostrar a lista de produtos individuais."""
    text = "📦 *Produtos Individuais*\n\nSelecione um produto para ver mais detalhes:"
    reply_markup = _get_individual_products_submenu()
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def _show_product_options(query: Update.callback_query, product_key: str) -> None:
    """Edita a mensagem para mostrar as opções de um produto específico."""
    product_label = MEDIA.get('produtos', {}).get(product_key, {}).get('label', product_key.capitalize())
    text = f"Você selecionou: *{product_label}*\n\nEscolha o que deseja ver:"
    reply_markup = _get_product_options_menu(product_key)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def _send_product_file(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE, product_key: str, file_type: str) -> None:
    """Encontra e envia um arquivo (foto, vídeo, documento) de um produto."""
    file_id = MEDIA.get('produtos', {}).get(product_key, {}).get(file_type)
    
    if not file_id:
        await query.answer("⚠️ Mídia não encontrada.", show_alert=True)
        return

    try:
        sender_map = {
            'foto': context.bot.send_photo,
            'video': context.bot.send_video,
            'documento': context.bot.send_document,
        }
        sender = sender_map.get(file_type)
        if sender:
            # Envia a mídia e, em caso de sucesso, edita a mensagem original para remover os botões.
            await sender(chat_id=query.message.chat.id, photo=file_id)
            await query.edit_message_text(f"✅ Mídia enviada! Para continuar, use o comando /produtos novamente.")
        else:
            raise ValueError(f"Tipo de arquivo desconhecido: {file_type}")

    except TelegramError as e:
        logger.error(f"Erro ao enviar arquivo '{file_type}' do produto '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar a mídia. Tente novamente.", show_alert=True)

async def _send_sales_pitch(query: Update.callback_query, product_key: str) -> None:
    """Envia a mensagem com o pitch de venda de um produto."""
    pitch_text = PITCH_DE_VENDA_TEXT.get(product_key)
    
    if not pitch_text:
        await query.answer("⚠️ Pitch de venda não encontrado.", show_alert=True)
        return
        
    try:
        # Envia o pitch e edita a mensagem original para remover os botões.
        await query.message.reply_text(pitch_text, parse_mode='Markdown')
        await query.edit_message_text("✅ Pitch de venda enviado! Para continuar, use o comando /produtos novamente.")
    except TelegramError as e:
        logger.error(f"Erro ao enviar pitch de venda para '{product_key}': {e}")
        await query.answer("⚠️ Ocorreu um erro ao enviar o texto. Tente novamente.", show_alert=True)


async def products_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Roteador inteligente para todos os callbacks que começam com 'products_'."""
    query = update.callback_query
    # Responde imediatamente ao clique para evitar a sensação de "travado" e duplo clique.
    await query.answer()

    try:
        data = query.data
        parts = data.split('_')
        # Estrutura do callback_data: "products_action_payload1_payload2"
        prefix, action = parts[0], parts[1]

        if action == 'main':
            await beneficiosprodutos(update, context)
        elif action == 'submenu':
            await _show_individual_products_submenu(query)
        elif action == 'show':
            product_key = parts[2]
            await _show_product_options(query, product_key)
        elif action == 'send':
            product_key, file_type = parts[2], parts[3]
            await _send_product_file(query, context, product_key, file_type)
        elif action == 'pitch':
            product_key = parts[2]
            await _send_sales_pitch(query, product_key)

    except (IndexError, TelegramError) as e:
        logger.error(f"Erro ao processar callback de produtos '{query.data}': {e}")
        try:
            # Em caso de erro, tenta de forma segura reverter para o menu principal.
            await query.edit_message_text("Ocorreu um erro, te redirecionando para o menu principal.", reply_markup=_get_main_menu())
        except TelegramError:
            pass # A mensagem original pode não existir mais.

# NOTA PARA INTEGRAÇÃO:
# Em main.py, o comando já deve estar registrado.
# Em core/handlers.py, substitua as rotas antigas por esta unificada:
# elif data.startswith('products_'):
#     await product_handlers.products_callback_handler(update, context)