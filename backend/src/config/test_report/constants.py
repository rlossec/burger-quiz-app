"""
Constantes de mapping pour la génération du rapport HTML de tests.

- MODEL_LABELS   : dossier de tests → libellé métier du modèle
- API_PATH_BY_RESOURCE : ressource → segment de chemin d'URL
- ENDPOINT_LABELS : (ressource, action) → libellé complet de l'endpoint
- MODEL_ORDER    : ordre d'affichage des modèles dans le rapport
"""

MODEL_LABELS: dict[str, str] = {
    "questions": "Questions",
    "nuggets": "Nuggets",
    "salt_or_pepper": "Sel ou poivre",
    "menu_themes": "Thème de menu",
    "menus": "Menus",
    "additions": "Addition",
    "deadly_burgers": "Burger de la mort",
    "burger_quizzes": "Burger Quiz",
}

API_PATH_BY_RESOURCE: dict[str, str] = {
    "questions": "questions",
    "nuggets": "nuggets",
    "salt_or_pepper": "salt-or-pepper",
    "menu_themes": "menu-themes",
    "menus": "menus",
    "additions": "additions",
    "deadly_burgers": "deadly-burgers",
    "burger_quizzes": "burger-quizzes",
}

# Actions reconnues et leurs verbes HTTP
_ACTIONS: dict[str, str] = {
    "list":   "GET",
    "detail": "GET",
    "create": "POST",
    "update": "PUT/PATCH",
    "delete": "DELETE",
}

# Suffixes de chemin selon l'action
_ACTION_PATH_SUFFIX: dict[str, str] = {
    "list":   "",
    "detail": "{id}/",
    "create": "",
    "update": "{id}/",
    "delete": "{id}/",
}


def build_endpoint_labels() -> dict[tuple[str, str], str]:
    """
    Génère dynamiquement le dictionnaire ENDPOINT_LABELS
    pour toutes les combinaisons (resource, action).
    """
    labels: dict[tuple[str, str], str] = {}
    for resource, api_path in API_PATH_BY_RESOURCE.items():
        for action, method in _ACTIONS.items():
            suffix = _ACTION_PATH_SUFFIX[action]
            labels[(resource, action)] = f"{method} /api/quiz/{api_path}/{suffix}"
    return labels


ENDPOINT_LABELS: dict[tuple[str, str], str] = build_endpoint_labels()

MODEL_ORDER: tuple[str, ...] = (
    "Questions",
    "Nuggets",
    "Sel ou poivre",
    "Thème de menu",
    "Menus",
    "Addition",
    "Burger de la mort",
    "Burger Quiz",
)