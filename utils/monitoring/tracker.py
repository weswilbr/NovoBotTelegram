# NOME DO ARQUIVO: utils/monitoring/tracker.py
# REFACTOR: Classe para rastrear o uso de comandos pelos usuários.
import logging
import threading
from collections import Counter
import json
import os

logger = logging.getLogger(__name__)

class UsageTracker:
    """Rastreia o uso de comandos do bot por usuários, salvando em um arquivo JSON."""
    def __init__(self, filename="usage_data.json"):
        self.filename = filename
        self.user_command_counts = Counter()
        self.lock = threading.Lock()
        self.load_data()

    def load_data(self):
        """Carrega os dados de uso do arquivo JSON."""
        with self.lock:
            if not os.path.exists(self.filename):
                return
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.user_command_counts = Counter({int(k): v for k, v in data.items()})
                logger.info(f"Dados de uso carregados de {self.filename}")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Erro ao carregar dados de uso: {e}. Começando com dados vazios.")
                self.user_command_counts = Counter()

    def save_data(self):
        """Salva os dados de uso no arquivo JSON."""
        with self.lock:
            try:
                with open(self.filename, 'w') as f:
                    json.dump(self.user_command_counts, f, indent=4)
            except Exception as e:
                logger.error(f"Erro ao salvar dados de uso: {e}")

    def increment_command_count(self, user_id: int):
        """Incrementa a contagem de comandos para um usuário e salva."""
        with self.lock:
            self.user_command_counts[user_id] += 1
        self.save_data()

    def get_top_users(self, top_n: int = 10) -> list[tuple[int, int]]:
        """Retorna os top N usuários por contagem de comandos."""
        with self.lock:
            return self.user_command_counts.most_common(top_n)

    def reset_data(self):
        """Reseta todos os dados de contagem de comandos."""
        with self.lock:
            self.user_command_counts.clear()
        self.save_data()
        logger.warning("Dados de uso foram resetados!")

