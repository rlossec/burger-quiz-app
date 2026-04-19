"""
Paramètres de requête (query string) typés pour les vues API.
"""


def parse_positive_int(
    raw: str | None,
    *,
    default: int,
    minimum: int = 1,
    maximum: int = 100,
) -> int:
    """
    Interprète un entier positif issu d'un query param (ex. ``limit``, ``page_size``).

    - ``None`` ou chaîne vide → ``default``.
    - Valeur non numérique → ``default``.
    - Résultat borné entre ``minimum`` et ``maximum`` (inclus).
    """
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(value, maximum))
