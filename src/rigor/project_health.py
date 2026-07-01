"""
Project health check for Project Aleph-Omega.

This module checks whether key generated artifacts, documentation files, source
modules, and tests exist.

The goal is reviewer readiness: someone opening the repo should be able to see
that the main research artifacts and verification reports are present.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class HealthCheckItem:
    """
    One project health check item.
    """

    path: str
    category: str
    required: bool = True

    def exists(self) -> bool:
        """
        Returns whether the path exists.
        """

        return Path(self.path).exists()

    def passed(self) -> bool:
        """
        Returns whether this health check passes.
        """

        if not self.required:
            return True

        return self.exists()

    def describe(self) -> str:
        """
        Returns a readable health check item.
        """

        return (
            f"HealthCheckItem\n"
            f"Path: {self.path}\n"
            f"Category: {self.category}\n"
            f"Required: {self.required}\n"
            f"Exists: {self.exists()}\n"
            f"Passed: {self.passed()}"
        )


@dataclass(frozen=True)
class ProjectHealthReport:
    """
    Full project health report.
    """

    items: Tuple[HealthCheckItem, ...]

    def item_count(self) -> int:
        """
        Counts health check items.
        """

        return len(self.items)

    def passed_items(self) -> Tuple[HealthCheckItem, ...]:
        """
        Returns passed items.
        """

        return tuple(item for item in self.items if item.passed())

    def failed_items(self) -> Tuple[HealthCheckItem, ...]:
        """
        Returns failed items.
        """

        return tuple(item for item in self.items if not item.passed())

    def health_passes(self) -> bool:
        """
        Returns whether all required checks pass.
        """

        return len(self.failed_items()) == 0

    def categories(self) -> Tuple[str, ...]:
        """
        Returns health categories.
        """

        return tuple(sorted({item.category for item in self.items}))

    def describe(self) -> str:
        """
        Returns a readable health report.
        """

        return (
            f"ProjectHealthReport\n"
            f"Items: {self.item_count()}\n"
            f"Passed: {len(self.passed_items())}\n"
            f"Failed: {len(self.failed_items())}\n"
            f"Health passes: {self.health_passes()}"
        )


class ProjectHealthChecker:
    """
    Builds and runs project health checks.
    """

    def required_items(self) -> Tuple[HealthCheckItem, ...]:
        """
        Returns required project health check items.
        """

        return (
            HealthCheckItem("README.md", "root"),
            HealthCheckItem("docs/rigor_track.md", "documentation"),
            HealthCheckItem("docs/research_abstract.md", "research_artifact"),
            HealthCheckItem("docs/theorem_inventory.md", "research_artifact"),
            HealthCheckItem("docs/architecture_map.md", "research_artifact"),
            HealthCheckItem("docs/final_research_memo.md", "research_artifact"),
            HealthCheckItem("docs/model_search_report.md", "model_search"),
            HealthCheckItem("docs/failure_lab_report.md", "failure_lab"),
            HealthCheckItem("docs/verification_report.md", "verification"),
            HealthCheckItem("src/rigor/finite_universe.py", "source"),
            HealthCheckItem("src/rigor/bridge.py", "source"),
            HealthCheckItem("src/rigor/preservation.py", "source"),
            HealthCheckItem("src/rigor/model_search.py", "source"),
            HealthCheckItem("src/rigor/failure_taxonomy.py", "source"),
            HealthCheckItem("src/rigor/claim_registry.py", "source"),
            HealthCheckItem("src/rigor/final_research_memo.py", "source"),
            HealthCheckItem("tests/test_rigor_finite_universe.py", "tests"),
            HealthCheckItem("tests/test_rigor_model_search.py", "tests"),
            HealthCheckItem("tests/test_rigor_failure_taxonomy.py", "tests"),
            HealthCheckItem("tests/test_rigor_verification_report.py", "tests"),
            HealthCheckItem("tests/test_rigor_final_research_memo.py", "tests"),
        )

    def run(self) -> ProjectHealthReport:
        """
        Runs the project health check.
        """

        return ProjectHealthReport(items=self.required_items())


if __name__ == "__main__":
    report = ProjectHealthChecker().run()

    print(report.describe())

    if report.failed_items():
        print()
        print("Failed items:")
        for item in report.failed_items():
            print("- " + item.path)
