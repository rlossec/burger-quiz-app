"""
Package test_report — génération du rapport HTML pour le runner de tests Django.

Modules :
- utils.py       : fonctions utilitaires (slug, format_traceback)
- constants.py   : labels métier, endpoints, ordre d'affichage
- parser.py      : parsing des identifiants de tests
- html_builder.py: construction du rapport HTML
"""

from .html_builder import build_html_report

__all__ = ["build_html_report"]