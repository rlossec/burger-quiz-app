"""
Runner de tests Django générant un rapport HTML après chaque exécution.

Configuration dans settings.py :
    TEST_RUNNER = "config.test_runner.HtmlReportTestRunner"
    TEST_REPORT_DIR = BASE_DIR / "reports"   # optionnel (défaut : BASE_DIR / "reports")
"""

import time
from pathlib import Path

from django.conf import settings
from django.test.runner import DiscoverRunner

from .test_report import build_html_report


class HtmlReportTestRunner(DiscoverRunner):
    """
    Sous-classe de DiscoverRunner qui écrit un rapport HTML dans TEST_REPORT_DIR
    après chaque exécution de la suite de tests.
    """

    def run_suite(self, suite, **kwargs):
        start = time.perf_counter()
        result = super().run_suite(suite, **kwargs)
        duration = time.perf_counter() - start

        self._write_report(result, suite, duration)
        return result

    def _report_dir(self) -> Path:
        report_dir = getattr(settings, "TEST_REPORT_DIR", None) or (settings.BASE_DIR / "reports")
        path = Path(report_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _write_report(self, result, suite, duration: float) -> None:
        report_path = self._report_dir() / "test-report.html"
        report_html = build_html_report(result, suite, duration)
        report_path.write_text(report_html, encoding="utf-8")

        if self.verbosity >= 1:
            self.log(f"\nRapport des tests écrit dans : {report_path}")
