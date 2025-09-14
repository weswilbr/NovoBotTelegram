# NOME DO ARQUIVO: core/persistence.py
# FEATURE: Implementação de persistência customizada usando Vercel KV (Redis)
# para salvar o estado de conversas e outros dados do bot.

import json
import redis
from telegram.ext import BasePersistence
from typing import Any, Dict, Optional

class KVPersistence(BasePersistence):
    """
    Usa um cliente Redis (conectado ao Vercel KV) para persistir os dados do bot.
    Isso é essencial para ConversationHandler em ambientes serverless.
    """
    def __init__(self, redis_client: redis.Redis):
        super().__init__(store_data=True, update_interval=1)
        self.redis_client = redis_client

    def _get_key(self, key_name: str) -> str:
        return f"bot_persistence:{key_name}"

    def _load_key(self, key_name: str) -> Optional[Dict]:
        key = self._get_key(key_name)
        try:
            raw_data = self.redis_client.get(key)
            if raw_data:
                return json.loads(raw_data.decode('utf-8'))
            return None
        except (redis.RedisError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar chave '{key}' do KV: {e}")
            return None

    def _save_key(self, key_name: str, data: Dict) -> None:
        key = self._get_key(key_name)
        try:
            self.redis_client.set(key, json.dumps(data))
        except (redis.RedisError, TypeError) as e:
            print(f"Erro ao salvar chave '{key}' no KV: {e}")

    async def get_bot_data(self) -> Dict[str, Any]:
        data = self._load_key("bot_data")
        return data if data else {}

    async def update_bot_data(self, data: Dict[str, Any]) -> None:
        self._save_key("bot_data", data)

    async def get_chat_data(self) -> Dict[int, Dict[str, Any]]:
        data = self._load_key("chat_data")
        # Redis armazena chaves como strings, precisamos converter de volta para int
        return {int(k): v for k, v in data.items()} if data else {}

    async def update_chat_data(self, chat_id: int, data: Dict[str, Any]) -> None:
        all_chat_data = self._load_key("chat_data") or {}
        all_chat_data[str(chat_id)] = data
        self._save_key("chat_data", all_chat_data)

    async def get_user_data(self) -> Dict[int, Dict[str, Any]]:
        data = self._load_key("user_data")
        # Redis armazena chaves como strings, precisamos converter de volta para int
        return {int(k): v for k, v in data.items()} if data else {}

    async def update_user_data(self, user_id: int, data: Dict[str, Any]) -> None:
        all_user_data = self._load_key("user_data") or {}
        all_user_data[str(user_id)] = data
        self._save_key("user_data", all_user_data)

    async def get_callback_data(self) -> Optional[Any]:
        # Não usado com frequência, mas necessário para a interface
        return None

    async def update_callback_data(self, data: Any) -> None:
        # Não usado com frequência, mas necessário para a interface
        pass
        
    async def get_conversations(self, name: str) -> Dict:
        data = self._load_key(f"conversation:{name}")
        # Converte as chaves (que são tuplas serializadas como string) de volta para tuplas
        return {tuple(json.loads(k)): v for k, v in data.items()} if data else {}

    async def update_conversation(
        self, name: str, key: tuple, new_state: Optional[object]
    ) -> None:
        all_convs = self._load_key(f"conversation:{name}") or {}
        # Serializa a tupla da chave para uma string JSON para ser usada como chave no Redis
        conv_key = json.dumps(key)
        
        if new_state is None:
            all_convs.pop(conv_key, None)
        else:
            all_convs[conv_key] = new_state
            
        self._save_key(f"conversation:{name}", all_convs)

    async def flush(self) -> None:
        # O salvamento já é feito a cada update, então flush não precisa fazer nada.
        pass