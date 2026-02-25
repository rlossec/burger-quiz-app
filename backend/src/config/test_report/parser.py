"""
Fonctions de parsing et de résolution des identifiants de tests unitaires Django.
"""

import unittest

from .constants import API_PATH_BY_RESOURCE, ENDPOINT_LABELS, MODEL_LABELS


def parse_test_id(test_id: str) -> tuple[str, str, str]:
    """
    Découpe un identifiant de test en (module_path, class_name, method_name).

    Exemple :
        "quiz.tests.additions.test_create.TestAdditionCreateEndpoint.test_create_duplicate"
        → ("quiz.tests.additions.test_create", "TestAdditionCreateEndpoint", "test_create_duplicate")
    """
    parts = test_id.split(".")
    if len(parts) < 3:
        return (test_id, "", "")
    return ".".join(parts[:-2]), parts[-2], parts[-1]


def module_to_model_and_endpoint(module_path: str) -> tuple[str, str]:
    """
    Résout un chemin de module en (model_label, endpoint_label).

    Exemple :
        "quiz.tests.additions.test_create" → ("Addition", "POST /api/quiz/additions/")

    Retourne ("Autres", module_path) si le module n'est pas reconnu.
    """
    prefix = "quiz.tests."
    if not module_path.startswith(prefix):
        return ("Autres", module_path or "?")

    parts = module_path[len(prefix):].split(".")
    if len(parts) < 2:
        return ("Autres", parts[0] if parts else "?")

    resource, action_part = parts[0], parts[1]
    action = action_part.removeprefix("test_")
    model_label = MODEL_LABELS.get(resource, resource)
    endpoint_label = ENDPOINT_LABELS.get(
        (resource, action),
        f"{action} /api/quiz/{API_PATH_BY_RESOURCE.get(resource, resource)}/",
    )
    return (model_label, endpoint_label)


def iter_leaf_tests(suite: unittest.TestSuite) -> list[unittest.TestCase]:
    """
    Itère récursivement sur les tests feuilles d'une suite.
    Compatible avec la structure de suites Django (ignore les None).
    """
    out: list[unittest.TestCase] = []
    try:
        tests = getattr(suite, "_tests", None) or (
            list(suite) if hasattr(suite, "__iter__") else []
        )
    except (TypeError, AttributeError):
        return out

    for test in tests or []:
        if test is None:
            continue
        if isinstance(test, unittest.TestSuite):
            out.extend(iter_leaf_tests(test))
        else:
            out.append(test)
    return out