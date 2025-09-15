# NOME DO ARQUIVO: features/products/data.py
# REFACTOR: Carrega todos os dados de arquivos YAML externos para fácil manutenção.

"""
Este módulo é responsável por carregar todos os dados de conteúdo
(produtos, mídias, textos, links, etc.) de arquivos .yml externos.
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List

def load_yaml(file_path: Path) -> Dict[str, Any]:
    """
    Função auxiliar para carregar um arquivo YAML de forma segura.
    Retorna um dicionário vazio se o arquivo não for encontrado.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de dados não encontrado em '{file_path}'.")
        return {}
    except yaml.YAMLError as e:
        print(f"ERRO: Erro ao parsear o arquivo YAML '{file_path}': {e}")
        return {}

# --- CONFIGURAÇÃO DE CAMINHOS ---

# AJUSTE IMPORTANTE:
# Sobe dois níveis (de 'products' para 'features', e de 'features' para a raiz 'NOVOBOTTELEGRAM')
# e então aponta para a pasta 'data'.
DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data'


# --- CARREGAMENTO CENTRALIZADO DOS DADOS ---

PRODUTOS: Dict[str, Dict[str, Any]] = load_yaml(DATA_DIR / 'products.yml')
MEDIA_GERAL: Dict[str, Dict[str, str]] = load_yaml(DATA_DIR / 'general_media.yml')
CONTEUDO: Dict[str, Any] = load_yaml(DATA_DIR / 'content.yml')


# --- EXPORTAÇÃO DE VARIÁVEIS PARA USO EM OUTROS MÓDULOS ---

CONVITES_TEXT: Dict[str, str] = CONTEUDO.get('convites', {})
GLOSSARIO_TERMS: Dict[str, str] = CONTEUDO.get('glossario', {})
POSITIONS: Dict[str, Dict[str, Any]] = CONTEUDO.get('positions', {})
TRAINING_MATERIALS: Dict[str, List[Dict[str, str]]] = CONTEUDO.get('training_materials', {})

_links: Dict[str, List[Dict[str, str]]] = CONTEUDO.get('links', {})
YOUTUBE_LINKS: List[Dict[str, str]] = _links.get('youtube', [])
TELEGRAM_LINKS: List[Dict[str, str]] = _links.get('telegram', [])
WHATSAPP_LINKS: List[Dict[str, str]] = _links.get('whatsapp', [])


# --- Validação Simples (Opcional, mas recomendado) ---
if not PRODUTOS:
    print("ALERTA DE CARREGAMENTO: Nenhum produto foi carregado. Verifique o arquivo 'products.yml'.")
if not CONTEUDO:
    print("ALERTA DE CARREGAMENTO: Nenhum conteúdo geral foi carregado. Verifique o arquivo 'content.yml'.")