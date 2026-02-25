
"""
Fonctions utilitaires partagées pour la génération du rapport HTML de tests.
"""

import html
import re


def format_traceback(tb_str: str, max_lines: int = 30) -> str:
    """Tronque et échappe un traceback pour insertion dans du HTML."""
    if not tb_str:
        return ""
    lines = tb_str.strip().split("\n")
    if len(lines) > max_lines:
        lines = lines[:max_lines] + [f"... ({len(lines) - max_lines} lignes supplémentaires)"]
    return html.escape("\n".join(lines))


def slug(value: str) -> str:
    """
    Génère un identifiant HTML sûr à partir d'une chaîne :
    minuscules, espaces et '/' remplacés par '-', caractères spéciaux supprimés.
    """
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s/]+", "-", value).strip("-").lower()
    return value or "section"