# NOME DO ARQUIVO: features/products/data.py
# Carrega YAMLs e expõe dicionários globais.

import logging
from pathlib import Path
from typing import Any, Dict, List

import yaml

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Função auxiliar
# --------------------------------------------------------------------------- #
def load_yaml(path: Path) -> Dict[str, Any]:
    """Lê um YAML no disco e devolve dict; nunca lança exceção."""
    try:
        text = path.read_text(encoding="utf-8")
        return yaml.safe_load(text) or {}
    except FileNotFoundError:
        logger.warning("Arquivo de dados não encontrado: %s", path)
    except yaml.YAMLError as err:
        logger.error("Erro ao parsear YAML %s: %s", path, err)
    return {}

# --------------------------------------------------------------------------- #
# Caminho para ./data
# --------------------------------------------------------------------------- #
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

# --------------------------------------------------------------------------- #
# Carregamento dos YAMLs
# --------------------------------------------------------------------------- #
PRODUTOS: Dict[str, Dict[str, Any]]  = load_yaml(DATA_DIR / "products.yml")
MEDIA_GERAL: Dict[str, Dict[str, str]] = load_yaml(DATA_DIR / "general_media.yml")
CONTEUDO: Dict[str, Any] = load_yaml(DATA_DIR / "content.yml")

# Alias legado
MEDIA = MEDIA_GERAL

# --------------------------------------------------------------------------- #
# Validações básicas
# --------------------------------------------------------------------------- #
if not PRODUTOS:
    logger.warning("Nenhum produto carregado. Verifique 'products.yml'.")

if not CONTEUDO:
    logger.warning("Nenhum conteúdo geral carregado. Verifique 'content.yml'.")

# Checa se cada produto tem 'label' (evita KeyError no menu)
for key, val in list(PRODUTOS.items()):
    if "label" not in val:
        logger.warning("Produto '%s' não possui 'label' — removido.", key)
        PRODUTOS.pop(key)

# --------------------------------------------------------------------------- #
# Exports específicos
# --------------------------------------------------------------------------- #
CONVITES_TEXT: Dict[str, str] = CONTEUDO.get("convites", {})
GLOSSARIO_TERMS: Dict[str, str] = CONTEUDO.get("glossario", {})
POSITIONS: Dict[str, Dict[str, Any]] = CONTEUDO.get("positions", {})
TRAINING_MATERIALS: Dict[str, List[Dict[str, str]]] = CONTEUDO.get("training_materials", {})

_links: Dict[str, List[Dict[str, str]]] = CONTEUDO.get("links", {})
YOUTUBE_LINKS:  List[Dict[str, str]] = _links.get("youtube", [])
TELEGRAM_LINKS: List[Dict[str, str]] = _links.get("telegram", [])
WHATSAPP_LINKS: List[Dict[str, str]] = _links.get("whatsapp", [])

__all__ = [
    "PRODUTOS", "MEDIA_GERAL", "MEDIA",
    "CONVITES_TEXT", "GLOSSARIO_TERMS", "POSITIONS",
    "TRAINING_MATERIALS", "YOUTUBE_LINKS", "TELEGRAM_LINKS", "WHATSAPP_LINKS",
]