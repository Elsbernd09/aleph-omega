"""
Research artifact model for Project ℵω.

This module defines reportable research artifacts that can be exported into
human-readable summaries, Markdown reports, and future papers.

The reporting layer does not create new proofs. It organizes the outputs of
the computational research system.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ArtifactKind(str, Enum):
    """
    Kind of research artifact.
    """

    AXIOM = "axiom"
    UNIVERSE = "universe"
    STATEMENT = "statement"
    SIMULATION_RESULT = "simulation_result"
    BRIDGE_TRANSLATION = "bridge_translation"
    DISTORTION_REPORT = "distortion_report"
    INTUITION = "intuition"
    COGNITIVE_MORPHISM = "cognitive_morphism"
    FORMALIZATION_GAP = "formalization_gap"
    LEAN_SKETCH = "lean_sketch"
    PROOF_OBLIGATION = "proof_obligation"
    FORMALIZATION_PLAN = "formalization_plan"
    META_THEORY_REPORT = "meta_theory_report"
    SYSTEM_SUMMARY = "system_summary"


class ArtifactStatus(str, Enum):
    """
    Status of a research artifact.
    """

    DRAFT = "draft"
    EXPERIMENTAL = "experimental"
    REVIEW_REQUIRED = "review_required"
    VALIDATED_BY_TESTS = "validated_by_tests"
    READY_FOR_REPORT = "ready_for_report"
    ARCHIVED = "archived"


class ArtifactRisk(str, Enum):
    """
    Risk level of using an artifact in a serious research claim.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass(frozen=True)
class ResearchArtifact:
    """
    A reportable artifact from the Project ℵω system.
    """

    title: str
    kind: ArtifactKind
    status: ArtifactStatus
    risk: ArtifactRisk
    summary: str
    key_points: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    source_layer: str = ""
    confidence_score: float = 0.0
    metadata: Optional[Dict[str, str]] = None

    def normalized_confidence(self) -> float:
        """
        Returns confidence clamped between 0 and 10.
        """

        return round(max(0.0, min(10.0, self.confidence_score)), 2)

    def requires_review(self) -> bool:
        """
        Returns whether the artifact should be reviewed before publication.
        """

        return (
            self.status == ArtifactStatus.REVIEW_REQUIRED
            or self.risk in {ArtifactRisk.HIGH, ArtifactRisk.EXTREME}
            or self.normalized_confidence() < 6.0
        )

    def markdown_section(self) -> str:
        """
        Converts the artifact into a Markdown section.
        """

        key_points = "\n".join(f"- {point}" for point in self.key_points) or "- none"
        limitations = "\n".join(f"- {item}" for item in self.limitations) or "- none"

        return (
            f"## {self.title}\n\n"
            f"**Kind:** {self.kind.value}\n\n"
            f"**Source layer:** {self.source_layer or 'not specified'}\n\n"
            f"**Status:** {self.status.value}\n\n"
            f"**Risk:** {self.risk.value}\n\n"
            f"**Confidence score:** {self.normalized_confidence()}\n\n"
            f"**Requires review:** {self.requires_review()}\n\n"
            f"### Summary\n\n"
            f"{self.summary}\n\n"
            f"### Key Points\n\n"
            f"{key_points}\n\n"
            f"### Limitations\n\n"
            f"{limitations}\n"
        )

    def describe(self) -> str:
        """
        Returns a readable text description.
        """

        return (
            f"ResearchArtifact: {self.title}\n"
            f"Kind: {self.kind.value}\n"
            f"Source layer: {self.source_layer or 'not specified'}\n"
            f"Status: {self.status.value}\n"
            f"Risk: {self.risk.value}\n"
            f"Confidence score: {self.normalized_confidence()}\n"
            f"Requires review: {self.requires_review()}\n"
            f"Summary: {self.summary}"
        )


@dataclass(frozen=True)
class ResearchArtifactCollection:
    """
    Collection of reportable research artifacts.
    """

    title: str
    artifacts: List[ResearchArtifact] = field(default_factory=list)
    summary: str = ""
    metadata: Optional[Dict[str, str]] = None

    def artifact_count(self) -> int:
        """
        Counts artifacts.
        """

        return len(self.artifacts)

    def review_required_count(self) -> int:
        """
        Counts artifacts requiring review.
        """

        return sum(1 for artifact in self.artifacts if artifact.requires_review())

    def average_confidence(self) -> float:
        """
        Computes average artifact confidence.
        """

        if not self.artifacts:
            return 0.0

        total = sum(artifact.normalized_confidence() for artifact in self.artifacts)
        return round(total / len(self.artifacts), 2)

    def artifacts_by_kind(self) -> Dict[str, int]:
        """
        Counts artifacts by kind.
        """

        counts: Dict[str, int] = {}

        for artifact in self.artifacts:
            key = artifact.kind.value
            counts[key] = counts.get(key, 0) + 1

        return counts

    def markdown(self) -> str:
        """
        Converts the collection into Markdown.
        """

        sections = "\n\n".join(
            artifact.markdown_section() for artifact in self.artifacts
        )

        kind_counts = "\n".join(
            f"- {kind}: {count}"
            for kind, count in sorted(self.artifacts_by_kind().items())
        ) or "- none"

        return (
            f"# {self.title}\n\n"
            f"{self.summary or 'No collection summary provided.'}\n\n"
            f"## Collection Metrics\n\n"
            f"- Artifact count: {self.artifact_count()}\n"
            f"- Review required count: {self.review_required_count()}\n"
            f"- Average confidence: {self.average_confidence()}\n\n"
            f"## Artifact Counts by Kind\n\n"
            f"{kind_counts}\n\n"
            f"{sections}\n"
        )

    def describe(self) -> str:
        """
        Returns a readable collection description.
        """

        return (
            f"ResearchArtifactCollection: {self.title}\n"
            f"Artifact count: {self.artifact_count()}\n"
            f"Review required count: {self.review_required_count()}\n"
            f"Average confidence: {self.average_confidence()}\n"
            f"Summary: {self.summary or 'none'}"
        )


def demo_artifact_collection() -> ResearchArtifactCollection:
    """
    Creates a small demo collection for checking the module.
    """

    artifact = ResearchArtifact(
        title="Demo System Summary",
        kind=ArtifactKind.SYSTEM_SUMMARY,
        status=ArtifactStatus.EXPERIMENTAL,
        risk=ArtifactRisk.MEDIUM,
        summary="A demonstration artifact for the reporting layer.",
        key_points=[
            "Shows how artifacts become Markdown sections.",
            "Tracks confidence, risk, and review requirements.",
        ],
        limitations=[
            "This is only a demo artifact.",
        ],
        source_layer="reporting",
        confidence_score=7.0,
    )

    return ResearchArtifactCollection(
        title="Demo Artifact Collection",
        artifacts=[artifact],
        summary="A demonstration collection for Phase 9A.",
    )


if __name__ == "__main__":
    collection = demo_artifact_collection()
    print(collection.describe())
    print()
    print(collection.markdown())
