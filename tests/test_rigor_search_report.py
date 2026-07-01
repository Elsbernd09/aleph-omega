"""
Tests for model-search report generation.
"""

from pathlib import Path

from src.rigor.finite_universe import SemanticFeature
from src.rigor.search_report import (
    CombinedModelSearchReport,
    ModelSearchReportBuilder,
)


def small_report():
    return ModelSearchReportBuilder().build(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )


def test_combined_model_search_report_exists():
    report = small_report()

    assert isinstance(report, CombinedModelSearchReport)
    assert report.total_cases() > 0
    assert "CombinedModelSearchReport" in report.describe()


def test_combined_report_counts():
    report = small_report()

    assert report.bridge_distortion_report.case_count() > 0
    assert report.satisfaction_report.case_count() > 0
    assert report.total_cases() == (
        report.bridge_distortion_report.case_count()
        + report.satisfaction_report.case_count()
    )


def test_bridge_theorem_survived_search():
    report = small_report()

    assert report.theorem_survived_bridge_search()
    assert report.bridge_distortion_counterexample_count() == 0


def test_markdown_contains_sections():
    report = small_report()
    markdown = ModelSearchReportBuilder().to_markdown(report)

    assert "# Project ℵω Finite Model-Search Report" in markdown
    assert "Bridge Distortion Theorem Search" in markdown
    assert "Satisfaction Preservation Search" in markdown
    assert "Correct Claim" in markdown


def test_write_markdown(tmp_path):
    report = small_report()
    output_path = tmp_path / "model_search_report.md"

    written = ModelSearchReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Finite Model-Search Report" in written.read_text()
