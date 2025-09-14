# NOME DO ARQUIVO: utils/monitoring/tracker.py
# REFACTOR: Modificado para usar Vercel KV (Redis) em vez de um arquivo JSON local.

import json
import os
import redis
from collections import defaultdict
import logging

# Configura um logger para este módulo
logger = logging.getLogger(__name__)

# --- Conexão com o Vercel KV ---
# Conecta-se ao Vercel KV usando a URL fornecida nas variáveis de ambiente.
# A biblioteca 'redis' sabe como lidar com a string de conexão 'rediss://...'
try:
    KV_URL = os.getenv("KV_URL")
    if not KV_URL:
        # Se a KV_URL não estiver definida, levantamos um erro para deixar claro.
        raise ValueError("KV_URL não está configurada nas variáveis de ambiente.")
    
    # Cria o cliente Redis a partir da URL.
    kv_client = redis.from_url(KV_URL)
    # Testa a conexão para garantir que está funcionando
    kv_client.ping()
    logger.info("Conexão com Vercel KV estabelecida com sucesso.")

except Exception as e:
    # Se a conexão falhar, o tracker funcionará em memória (não persistirá dados).
    # Isso permite que o bot continue funcionando, mas sem salvar as estatísticas.
    logger.warning(f"Não foi possível conectar ao Vercel KV: {e}. O UsageTracker funcionará em modo de memória (não persistente).")
    kv_client = None

class UsageTracker:
    def __init__(self):
        """Inicializa o tracker, definindo a chave que será usada no banco de dados KV."""
        # A chave onde vamos armazenar todos os dados de uso no Vercel KV.
        self.redis_key = "bot_usage_data"

    def _load_data(self) -> defaultdict:
        """
        Carrega os dados de contagem de usuários do Vercel KV.
        Retorna um dicionário com os dados ou um dicionário vazio se não houver dados.
        """
        if not kv_client:
            return defaultdict(int) # Retorna dicionário vazio se não houver conexão com KV

        try:
            # Pega os dados da chave no KV
            data = kv_client.get(self.redis_key)
            if data:
                # Os dados são armazenados como uma string JSON, então precisamos decodificá-los
                user_counts = json.loads(data.decode('utf-8'))
                return defaultdict(int, user_counts)
            return defaultdict(int) # Retorna dicionário vazio se a chave não existir
        except Exception as e:
            logger.error(f"Falha ao carregar dados do Vercel KV: {e}")
            return defaultdict(int)

    def _save_data(self, user_counts: dict) -> None:
        """
        Salva o dicionário de contagem de usuários no Vercel KV.
        """
        if not kv_client:
            return # Não faz nada se não houver conexão com KV

        try:
            # Converte o dicionário para uma string JSON e salva no KV
            kv_client.set(self.redis_key, json.dumps(user_counts))
        except Exception as e:
            logger.error(f"Falha ao salvar dados no Vercel KV: {e}")
            
    def track_usage(self, user_id: int) -> None:
        """
        Rastreia e incrementa o uso de um comando por um usuário.
        """
        user_id_str = str(user_id)
        user_counts = self._load_data()
        user_counts[user_id_str] += 1
        self._save_data(user_counts)
        logger.info(f"Uso rastreado para o usuário {user_id_str}. Total: {user_counts[user_id_str]}")

    def get_top_users(self, top_n: int = 10) -> list:
        """
        Busca os dados do Vercel KV e retorna uma lista com os N usuários mais ativos.
        """
        user_counts = self._load_data()
        if not user_counts:
            return []
        
        # Ordena os itens do dicionário pelo valor (contagem) em ordem decrescente
        sorted_users = sorted(user_counts.items(), key=lambda item: item[1], reverse=True)
        
        # Retorna os N primeiros da lista ordenada
        return sorted_users[:top_n]

    def reset_data(self) -> None:
        """
        Apaga todos os dados de uso do Vercel KV, resetando a contagem.
        """
        if not kv_client:
            logger.warning("Tracker em modo de memória. Não há dados persistidos para resetar.")
            return

        try:
            # Deleta a chave do banco de dados
            kv_client.delete(self.redis_key)
            logger.info("Dados de uso foram resetados com sucesso no Vercel KV.")
        except Exception as e:
            logger.error(f"Falha ao resetar dados no Vercel KV: {e}")