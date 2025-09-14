# NOME DO ARQUIVO: utils/monitoring/tracker.py
# REFACTOR: Modificado para salvar um objeto contendo nome e contagem no Vercel KV.

import json
import os
import redis
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

# --- Conexão com o Vercel KV ---
try:
    KV_URL = os.getenv("KV_URL")
    if not KV_URL:
        raise ValueError("KV_URL não está configurada.")
    kv_client = redis.from_url(KV_URL)
    kv_client.ping()
    logger.info("Conexão com Vercel KV estabelecida com sucesso.")
except Exception as e:
    logger.warning(f"Não foi possível conectar ao Vercel KV: {e}. O UsageTracker funcionará em modo de memória.")
    kv_client = None

class UsageTracker:
    def __init__(self):
        self.redis_key = "bot_usage_data_v2" # Usamos uma nova chave para a nova estrutura de dados

    def _load_data(self) -> dict:
        """Carrega os dados completos do Vercel KV."""
        if not kv_client:
            return {}
        try:
            data = kv_client.get(self.redis_key)
            return json.loads(data.decode('utf-8')) if data else {}
        except Exception as e:
            logger.error(f"Falha ao carregar dados do Vercel KV: {e}")
            return {}

    def _save_data(self, all_user_data: dict) -> None:
        """Salva os dados completos no Vercel KV."""
        if not kv_client:
            return
        try:
            kv_client.set(self.redis_key, json.dumps(all_user_data))
        except Exception as e:
            logger.error(f"Falha ao salvar dados no Vercel KV: {e}")
            
    def track_usage(self, user_id: int, first_name: str) -> None:
        """Rastreia o uso, salvando ID, nome e incrementando a contagem."""
        user_id_str = str(user_id)
        all_data = self._load_data()
        
        # Pega os dados do usuário atual ou cria um novo registro
        user_data = all_data.get(user_id_str, {'name': first_name, 'count': 0})
        
        # Atualiza o nome (caso o usuário tenha mudado) e incrementa a contagem
        user_data['name'] = first_name
        user_data['count'] += 1
        
        # Coloca os dados atualizados de volta no objeto principal
        all_data[user_id_str] = user_data
        
        self._save_data(all_data)
        logger.info(f"Uso rastreado para {first_name} ({user_id_str}). Total: {user_data['count']}")

    def get_top_users(self, top_n: int = 10) -> list:
        """Retorna uma lista dos N usuários mais ativos, já com nomes."""
        all_data = self._load_data()
        if not all_data:
            return []
        
        # Ordena os usuários pela contagem (item[1]['count'])
        sorted_users = sorted(all_data.items(), key=lambda item: item[1]['count'], reverse=True)
        
        return sorted_users[:top_n]

    def reset_data(self) -> None:
        """Apaga todos os dados de uso do Vercel KV."""
        if not kv_client:
            return
        try:
            kv_client.delete(self.redis_key)
            logger.info("Dados de uso foram resetados com sucesso no Vercel KV.")
        except Exception as e:
            logger.error(f"Falha ao resetar dados no Vercel KV: {e}")