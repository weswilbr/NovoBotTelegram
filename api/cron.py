# NOME DO ARQUIVO: api/cron.py
from http.server import BaseHTTPRequestHandler
import asyncio
from telegram import Bot
from config import BOT_TOKEN, CANAL_ID_2 # Precisamos dos IDs aqui
from utils.monitoring.motivation import enviar_motivacao # Importa a função base

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        bot = Bot(token=BOT_TOKEN)
        # Executa a função assíncrona
        asyncio.run(enviar_motivacao(bot, CANAL_ID_2))
        
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Cron job executed.'.encode('utf-8'))
        return