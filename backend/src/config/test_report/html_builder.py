"""
Construction du rapport HTML à partir des résultats d'un TestResult Django.

Point d'entrée : build_html_report(result, suite, duration_seconds) -> str
"""

import html
import unittest
from collections import defaultdict
from datetime import datetime

from django.test.utils import iter_test_cases

from .constants import MODEL_ORDER
from .parser import iter_leaf_tests, module_to_model_and_endpoint, parse_test_id
from .utils import format_traceback, slug

# ---------------------------------------------------------------------------
# Types internes
# ---------------------------------------------------------------------------

GroupData = dict[str, list]  # {"passed": [], "failures": [...], "errors": [...], "skipped": [...]}
Groups = dict[tuple[str, str], GroupData]


# ---------------------------------------------------------------------------
# Collecte des résultats
# ---------------------------------------------------------------------------

def _collect_groups(result: unittest.TestResult, leaf_tests: list[unittest.TestCase]) -> tuple[Groups, set[str], set[str]]:
    """
    Construit le dictionnaire groups[(model, endpoint)] → {passed, failures, errors, skipped}
    et retourne également les ensembles d'IDs de base en échec et ignorés.
    """
    failed_base_ids: set[str] = {
        t.id().split(" (")[0]
        for t, _ in (*result.failures, *result.errors)
    }
    skipped_base_ids: set[str] = {
        t.id().split(" (")[0]
        for t, _ in (getattr(result, "skipped", None) or [])
    }

    groups: Groups = defaultdict(lambda: {"passed": [], "failures": [], "errors": [], "skipped": []})

    for test, tb in result.failures:
        mod, _, _ = parse_test_id(test.id())
        groups[module_to_model_and_endpoint(mod)]["failures"].append((test, tb))

    for test, tb in result.errors:
        mod, _, _ = parse_test_id(test.id())
        groups[module_to_model_and_endpoint(mod)]["errors"].append((test, tb))

    for test, reason in (getattr(result, "skipped", None) or []):
        mod, _, _ = parse_test_id(test.id())
        groups[module_to_model_and_endpoint(mod)]["skipped"].append((test, reason))

    for test in leaf_tests:
        base_id = test.id().split(" (")[0]
        if base_id in failed_base_ids or base_id in skipped_base_ids:
            continue
        mod, _, method_name = parse_test_id(test.id())
        groups[module_to_model_and_endpoint(mod)]["passed"].append(method_name)

    return groups, failed_base_ids, skipped_base_ids


# ---------------------------------------------------------------------------
# Rendu HTML des lignes de tableau
# ---------------------------------------------------------------------------

def _render_table_rows(g: GroupData) -> str:
    """
    Génère les <tr> du tableau de tests pour un endpoint.
    Ordre : réussis → échecs → erreurs → ignorés.
    """
    rows: list[str] = []

    for name in sorted(g["passed"]):
        rows.append(
            f'<tr>'
            f'<td>{html.escape(name)}</td>'
            f'<td><span class="badge badge-ok">✓ Success</span></td>'
            f'<td></td>'
            f'</tr>'
        )
    for test, tb in g["failures"]:
        method = parse_test_id(test.id())[2]
        rows.append(
            f'<tr>'
            f'<td>{html.escape(method)}</td>'
            f'<td><span class="badge badge-fail">✗ Fail</span></td>'
            f'<td><pre>{format_traceback(tb)}</pre></td>'
            f'</tr>'
        )
    for test, tb in g["errors"]:
        method = parse_test_id(test.id())[2]
        rows.append(
            f'<tr>'
            f'<td>{html.escape(method)}</td>'
            f'<td><span class="badge badge-error">⚠ Error</span></td>'
            f'<td><pre>{format_traceback(tb)}</pre></td>'
            f'</tr>'
        )
    for test, reason in g["skipped"]:
        method = parse_test_id(test.id())[2]
        rows.append(
            f'<tr>'
            f'<td>{html.escape(method)}</td>'
            f'<td><span class="badge badge-skip">— Skipped</span></td>'
            f'<td>{html.escape(str(reason))}</td>'
            f'</tr>'
        )
    return "".join(rows)


def _render_endpoint_section(model_label: str, endpoint_label: str, g: GroupData) -> str:
    ep_id = "endpoint-" + slug(model_label) + "-" + slug(endpoint_label)
    total = len(g["passed"]) + len(g["failures"]) + len(g["errors"]) + len(g["skipped"])

    if not total:
        body = '<p class="meta">No tests.</p>'
    else:
        rows = _render_table_rows(g)
        body = (
            f'<table>'
            f'<thead><tr><th>Méthode</th><th>Statut</th><th>Détail</th></tr></thead>'
            f'<tbody>{rows}</tbody>'
            f'</table>'
        )
    return (
        f'<section class="test-group" id="{ep_id}">'
        f'<h3>{html.escape(endpoint_label)}</h3>'
        f'{body}'
        f'</section>'
    )


def _render_model_section(
    model_label: str,
    endpoints: list[tuple[str, GroupData]],
) -> tuple[str, str]:
    """
    Retourne (nav_item_html, content_section_html) pour un modèle donné.
    """
    section_id = "section-" + slug(model_label)
    endpoint_blocks = []
    nav_endpoint_links: list[str] = []

    for endpoint_label, g in sorted(endpoints, key=lambda x: x[0]):
        ep_id = "endpoint-" + slug(model_label) + "-" + slug(endpoint_label)
        nav_endpoint_links.append(
            f'<a href="#{ep_id}" class="nav-endpoint">{html.escape(endpoint_label)}</a>'
        )
        endpoint_blocks.append(_render_endpoint_section(model_label, endpoint_label, g))

    nav_item = (
        f'<div class="nav-model">'
        f'<div class="nav-model-title"><a href="#{section_id}">{html.escape(model_label)}</a></div>'
        f'<div class="nav-endpoints">{"".join(nav_endpoint_links)}</div>'
        f'</div>'
    )
    content_section = (
        f'<section class="model-section" id="{section_id}">'
        f'<h2>{html.escape(model_label)}</h2>'
        f'{"".join(endpoint_blocks)}'
        f'</section>'
    )
    return nav_item, content_section


# ---------------------------------------------------------------------------
# Point d'entrée public
# ---------------------------------------------------------------------------

def build_html_report(
    result: unittest.TestResult,
    suite: unittest.TestSuite,
    duration_seconds: float,
) -> str:
    """
    Construit et retourne le rapport de tests complet en HTML.
    """
    try:
        leaf_tests = list(iter_test_cases(suite))
    except (TypeError, AttributeError):
        leaf_tests = iter_leaf_tests(suite)

    groups, failed_base_ids, skipped_base_ids = _collect_groups(result, leaf_tests)

    # Calcul des totaux (au niveau méthode, sans doublons sous-tests)
    all_method_ids = {t.id().split(" (")[0] for t in leaf_tests}
    total = len(all_method_ids) if all_method_ids else result.testsRun
    passed_count = max(0, len(all_method_ids - failed_base_ids - skipped_base_ids)) if all_method_ids else max(0, total - len(failed_base_ids) - len(skipped_base_ids))
    failed_count = len(failed_base_ids)
    failure_count = len(result.failures)
    error_count = len(result.errors)
    skipped_count = len(skipped_base_ids)

    nav_items: list[str] = []
    content_sections: list[str] = []

    # Modèles dans l'ordre défini
    for model_label in MODEL_ORDER:
        endpoints = [
            (ep_label, g)
            for (m, ep_label), g in groups.items()
            if m == model_label
        ]
        if not endpoints:
            continue
        nav_item, section = _render_model_section(model_label, endpoints)
        nav_items.append(nav_item)
        content_sections.append(section)

    # Modèles hors ordre (ex. "Autres")
    other_models: dict[str, list[tuple[str, GroupData]]] = defaultdict(list)
    for (model_label, endpoint_label), g in groups.items():
        if model_label not in MODEL_ORDER:
            other_models[model_label].append((endpoint_label, g))

    for model_label in sorted(other_models):
        nav_item, section = _render_model_section(model_label, other_models[model_label])
        nav_items.append(nav_item)
        content_sections.append(section)

    return _render_html_page(
        nav_html="\n".join(nav_items),
        content_html="\n".join(content_sections),
        total=total,
        passed_count=passed_count,
        failure_count=failure_count,
        error_count=error_count,
        skipped_count=skipped_count,
        duration_seconds=duration_seconds,
    )


# ---------------------------------------------------------------------------
# Template HTML
# ---------------------------------------------------------------------------

def _render_html_page(
    *,
    nav_html: str,
    content_html: str,
    total: int,
    passed_count: int,
    failure_count: int,
    error_count: int,
    skipped_count: int,
    duration_seconds: float,
) -> str:
    now = datetime.now()
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de tests — {now.strftime("%Y-%m-%d %H:%M")}</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; color: #111827; background: #f8fafc; }}
        .layout {{ display: flex; gap: 1.5rem; max-width: 1280px; margin: 0 auto; padding: 1.5rem 2rem; }}

        /* Navigation */
        .nav {{
            flex: 0 0 230px;
            position: sticky;
            top: 1rem;
            align-self: start;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 1rem;
            max-height: 90vh;
            overflow-y: auto;
            font-size: 0.875rem;
        }}
        .nav a {{ display: block; color: #2563eb; text-decoration: none; padding: 0.2rem 0; }}
        .nav a:hover {{ text-decoration: underline; color: #1d4ed8; }}
        .nav-model {{ margin-bottom: 0.6rem; }}
        .nav-model-title {{ font-weight: 600; }}
        .nav-endpoints {{ margin-left: 0.8rem; }}
        .nav-endpoint {{ color: #4b5563 !important; font-size: 0.8rem; }}

        /* Contenu principal */
        .content {{ flex: 1; min-width: 0; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.25rem; }}
        h2 {{ font-size: 1.15rem; color: #1f2937; margin-top: 2rem; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.4rem; }}
        h3 {{ font-size: 0.95rem; color: #374151; margin: 1.25rem 0 0.4rem; }}
        .meta {{ color: #6b7280; font-size: 0.875rem; margin-bottom: 0.75rem; }}

        /* Badges */
        .summary {{ display: flex; gap: 0.75rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }}
        .badge {{ display: inline-block; padding: 0.3rem 0.7rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; }}
        .badge-total  {{ background: #e0e7ff; color: #3730a3; }}
        .badge-ok     {{ background: #d1fae5; color: #065f46; }}
        .badge-fail   {{ background: #ffedd5; color: #9a3412; }}
        .badge-error  {{ background: #fee2e2; color: #991b1b; }}
        .badge-skip   {{ background: #fef3c7; color: #92400e; }}

        /* Sections */
        section.model-section {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1.5rem; }}
        section.test-group {{ margin-bottom: 1rem; }}
        section.test-group h3 {{ border-bottom: 1px solid #f3f4f6; padding-bottom: 0.25rem; }}

        /* Tableau */
        table {{ border-collapse: collapse; width: 100%; margin-top: 0.5rem; font-size: 0.875rem; }}
        th {{ background: #f9fafb; color: #374151; font-weight: 600; text-align: left; padding: 0.5rem 0.75rem; border: 1px solid #e5e7eb; }}
        td {{ padding: 0.45rem 0.75rem; border: 1px solid #e5e7eb; vertical-align: top; }}
        tr:hover td {{ background: #f9fafb; }}

        pre {{ margin: 0; white-space: pre-wrap; font-size: 0.8rem; color: #374151; }}
    </style>
</head>
<body>
<div class="layout">
    <nav class="nav" aria-label="Sections du rapport">
        <a href="#top" style="font-weight:600;">⬆ Haut de page</a>
        <hr style="margin:0.5rem 0; border:none; border-top:1px solid #e5e7eb;">
        {nav_html}
    </nav>
    <main class="content" id="top">
        <h1>Rapport de tests</h1>
        <p class="meta">
            Généré le {now.strftime("%Y-%m-%d à %H:%M:%S")} — Durée : {duration_seconds:.2f} s
        </p>
        <div class="summary">
            <span class="badge badge-total">{total} tests</span>
            <span class="badge badge-ok">{passed_count} réussis</span>
            <span class="badge badge-fail">{failure_count} échoués</span>
            <span class="badge badge-error">{error_count} erreurs</span>
            <span class="badge badge-skip">{skipped_count} ignorés</span>
        </div>
        {content_html}
    </main>
</div>
</body>
</html>
"""