# NOME DO ARQUIVO: features/products/data.py
# REFACTOR: Carrega todos os dados de arquivos YAML externos para fácil manutenção.

"""
Este módulo é responsável por carregar todos os dados de conteúdo
(produtos, mídias, textos, links, etc.) a partir de arquivos .yml externos.

Seus principais pontos:
• Carrega os YAMLs da pasta `data/` (na raiz do projeto).
• Expõe variáveis globais que podem ser importadas livremente pelos demais módulos.
• Mantém um alias `MEDIA` → `MEDIA_GERAL` para retrocompatibilidade.
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List


# --------------------------------------------------------------------------- #
# Função auxiliar
# --------------------------------------------------------------------------- #
def load_yaml(file_path: Path) -> Dict[str, Any]:
    """
    Carrega de forma segura um arquivo YAML.
    • Retorna dicionário vazio se o arquivo não existir.
    • Exibe aviso em caso de erro de parsing.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        print(f"AVISO: Arquivo de dados não encontrado em '{file_path}'.")
        return {}
    except yaml.YAMLError as e:
        print(f"ERRO: Falha ao parsear o YAML '{file_path}': {e}")
        return {}


# --------------------------------------------------------------------------- #
# Configuração de caminhos
# --------------------------------------------------------------------------- #
# Sobe dois níveis (products → features → raiz) e aponta para a pasta `data/`
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


# --------------------------------------------------------------------------- #
# Carregamento centralizado dos dados
# --------------------------------------------------------------------------- #
PRODUTOS: Dict[str, Dict[str, Any]] = load_yaml(DATA_DIR / "products.yml")
MEDIA_GERAL: Dict[str, Dict[str, str]] = load_yaml(DATA_DIR / "general_media.yml")
MEDIA = MEDIA_GERAL   # ← Alias para compatibilidade com código legado
CONTEUDO: Dict[str, Any] = load_yaml(DATA_DIR / "content.yml")


# --------------------------------------------------------------------------- #
# Exportação de variáveis específicas
# --------------------------------------------------------------------------- #
CONVITES_TEXT: Dict[str, str] = CONTEUDO.get("convites", {})
GLOSSARIO_TERMS: Dict[str, str] = CONTEUDO.get("glossario", {})
POSITIONS: Dict[str, Dict[str, Any]] = CONTEUDO.get("positions", {})
TRAINING_MATERIALS: Dict[str, List[Dict[str, str]]] = CONTEUDO.get("training_materials", {})

_links: Dict[str, List[Dict[str, str]]] = CONTEUDO.get("links", {})
YOUTUBE_LINKS: List[Dict[str, str]] = _links.get("youtube", [])
TELEGRAM_LINKS: List[Dict[str, str]] = _links.get("telegram", [])
WHATSAPP_LINKS: List[Dict[str, str]] = _links.get("whatsapp", [])


# --------------------------------------------------------------------------- #
# Validação simples (opcional, mas recomendada)
# --------------------------------------------------------------------------- #
if not PRODUTOS:
    print("ALERTA: Nenhum produto foi carregado. Verifique 'products.yml'.")

if not CONTEUDO:
    print("ALERTA: Nenhum conteúdo geral foi carregado. Verifique 'content.yml'.")