"""
Tests for project health checks.
"""

from src.rigor.project_health import (
    HealthCheckItem,
    ProjectHealthChecker,
    ProjectHealthReport,
)


def test_health_check_item_describe():
    item = HealthCheckItem("README.md", "root")

    assert item.exists()
    assert item.passed()
    assert "HealthCheckItem" in item.describe()


def test_project_health_report_builds():
    report = ProjectHealthChecker().run()

    assert isinstance(report, ProjectHealthReport)
    assert report.item_count() > 0
    assert "ProjectHealthReport" in report.describe()


def test_project_health_passes():
    report = ProjectHealthChecker().run()

    assert report.health_passes()
    assert len(report.failed_items()) == 0


def test_project_health_categories():
    report = ProjectHealthChecker().run()
    categories = report.categories()

    assert "source" in categories
    assert "tests" in categories
    assert "documentation" in categories
    assert "research_artifact" in categories
