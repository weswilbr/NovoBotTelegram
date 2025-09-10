# NOME DO ARQUIVO: features/products/data.py
# REFACTOR: Arquivo central de dados, contendo todos os file_ids, textos e dicionários de mídia.
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton

# --- Dicionários de Mídia (File IDs) ---
MEDIA = {
    'bonusconstrutormidias': {
        'video1': 'BAACAgEAAxkBAAJAU2fGAtnueBNRnb1LCqFFFfHG35OYAAJcBQACS1kxRuel2nL4TjefNgQ',
        'documento': 'BQACAgEAAxkBAAJAVWfGBGDBfHcAAXBT7LRKfZTnTKNG7QACYAUAAktZMUbZVJlfL5F_9jYE'
    },
    'opportunity_files': {
        'arquivo_plano_compacto': 'BAACAgEAAxkBAAI_O2fBBcXgtR8YPZI5RIBr3xAtVXL9AALABAACTIwJRlyKEctv90EgNgQ',
        'plano_completo_slide': 'BQACAgEAAx0EfAGLsgACSxRnr5nGeVv-__3METe2NzeR-oTtiAACXwQAAqDHgEU0dMt3DK7pUjYE',
        'powerpoint_apresentacao': 'BQACAgEAAxkBAAInamcqBv7kMWB-1qsSFUCygOHPKpwKAALqAwAC_V5RRVNyVvuFLupaNgQ',
        'arquivo_por_que_4life': 'BAACAgEAAx0CfAGLsgACJzhnM-pUhPUFq2DUAZJjnpaPBrQHigACKAUAArbsoUXOgdYZchJLCDYE'
    },
    'fabrica4life': {
        'armazem': 'BAACAgEAAxkBAAIBMGbncmJda7Sz-CPPc4unHFYjinjdAAK6CwACz0RBR_6nHEgo0YTmNgQ',
        'envase': 'BAACAgEAAxkBAAIBMmbndcrrkMOWppQGRixAh_CbE4oeAAK7CwACz0RBRypfMI6d_CjQNgQ',
        'novafabrica': ['BAACAgEAAxkBAAIBNGbndj-Sl43gh_kdQLBXKhkqSc6AAAK8CwACz0RBR6FFUzlAx6JANgQ']
    },
    'fatorestransf': {
        'video1': {'type': 'video', 'id': 'BAACAgEAAxkBAAJJMGfqtNj0QxKXG4FOpQS95NmJXcupAAJKBgAC-9pZR5ORbjj6QwSVNgQ'},
        'video2': {'type': 'video', 'id': 'BAACAgEAAxkBAAJB8WfOAhRPVUK8u9LxuB-BSIXDPfTKAALSBAACynwwRMxkekB46LmzNgQ'},
        'video3': {'type': 'video', 'id': 'BAACAgEAAxkBAAIyi2c7eP1__N6H9Wwz0iWXMrOx6BwqAAJTBAACI1_ZRc1ewElkbwT5NgQ'},
        'table': {'type': 'document', 'id': 'BQACAgEAAxkBAAIw6Gc4xcpWr6KivsAiGUwOpwcID0wxAALjBAAChl_IRdQoqw0PYFCgNgQ'},
    },
    'reading_guide': {
        'portugues': "BQACAgEAAxkBAAIV92cIZX67GGW9AxvBMhPqtuutcfbDAAImAgAC2g0gRaHTh5Ck9Uh9NgQ",
        'espanhol': "BQACAgEAAxkBAAIV-WcIZbffVCL1686U7aoa0uDt18wZAAInAgAC2g0gRbpjJIA6L173NgQ"
    },
    # ... e assim por diante para todos os outros file_ids
}

# --- Dicionários de Textos e Dados Estruturados ---

PITCH_DE_VENDA_TEXT = {
    'beneficioriovidaburst': "🫐 *RioVida Burst 4Life*: Saúde e sabor! 💥...",
    # ...
}

CONVITES_TEXT = {
    'convite_1': "📈 Convite Profissional\n\nOi [Nome do Convidado], ...",
    # ...
}

GLOSSARIO_TERMS = {
    'upline': '**🔝 Upline:** ...',
    # ...
}

POSITIONS = {
    "Associate": { "emoji": "🔹", "nome_curto": "A", "pv_mensal": 50, "..."},
    # ...
}

EVENTOS = {
    "Boa Vista 🇧🇷": {
        "nome": "Boa Vista 🇧🇷",
        "file_id_foto": "AgACAgEAAxkBAAImKGcou0nzeJOY5mCvomwaLphxCV_nAAJJrTEbrGlARajSxbtHP1ucAQADAgADeQADNgQ",
        "texto": "Você já se perguntou...",
        "data_hora": datetime(2024, 11, 6, 20, 0),
        "duracao": timedelta(hours=1),
        "status": "off",
        "botao": InlineKeyboardButton("Boa Vista 🇧🇷", callback_data="evento_Boa Vista 🇧🇷")
    },
    # ...
}

FRASES_MOTIVACIONAIS = [
    "🌟 Confie na sua jornada! ...",
    # ...
]

YOUTUBE_LINKS = [("Dr José Benjamín Pérez", "https://www.youtube.com/...")]
TELEGRAM_LINKS = [("El Equipo de Triunfo (Oficial)", "https://t.me/...")]
WHATSAPP_LINKS = [("El Equipo de Triunfo", "https://whatsapp.com/...")]

TRAINING_MATERIALS = {
    'apoio': [{"title": "📄 Manejo de Objeções", "file_id": '...'}],
    'tutoriais': [{"title": "🎥 Simular Preço Produto no APP", "file_id": '...'}]
}

