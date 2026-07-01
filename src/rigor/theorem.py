"""
Bridge Distortion Theorem model for Project ℵω.

This module states and checks the finite Bridge Distortion Theorem in the
small rigor-track setting.

The theorem is not presented as a deep breakthrough yet. It is the first
precise theorem candidate extracted from the Project ℵω architecture.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge
from src.rigor.distortion import BridgeDistortionReport, DistortionAnalyzer


class TheoremStatus(str, Enum):
    """
    Status of a theorem check.
    """

    VERIFIED_FOR_INSTANCE = "verified_for_instance"
    VACUOUSLY_TRUE_FOR_INSTANCE = "vacuously_true_for_instance"
    FAILED_FOR_INSTANCE = "failed_for_instance"


@dataclass(frozen=True)
class TheoremHypothesis:
    """
    Hypotheses for the finite Bridge Distortion Theorem.

    H1: the bridge is total
    H2: the source universe supports at least one feature absent from the target
    H3: at least one source statement requires an absent feature
    """

    bridge_is_total: bool
    feature_mismatch_exists: bool
    statement_uses_absent_feature: bool

    def holds(self) -> bool:
        """
        Returns whether all hypotheses hold.
        """

        return (
            self.bridge_is_total
            and self.feature_mismatch_exists
            and self.statement_uses_absent_feature
        )

    def describe(self) -> str:
        """
        Returns a readable hypothesis description.
        """

        return (
            "TheoremHypothesis\n"
            f"Bridge is total: {self.bridge_is_total}\n"
            f"Feature mismatch exists: {self.feature_mismatch_exists}\n"
            f"Statement uses absent feature: {self.statement_uses_absent_feature}\n"
            f"All hypotheses hold: {self.holds()}"
        )


@dataclass(frozen=True)
class TheoremConclusion:
    """
    Conclusion for the finite Bridge Distortion Theorem.

    C: the bridge has at least one distortion witness.
    """

    distortion_witness_exists: bool

    def holds(self) -> bool:
        """
        Returns whether the conclusion holds.
        """

        return self.distortion_witness_exists

    def describe(self) -> str:
        """
        Returns a readable conclusion description.
        """

        return (
            "TheoremConclusion\n"
            f"Distortion witness exists: {self.distortion_witness_exists}"
        )


@dataclass(frozen=True)
class TheoremCheck:
    """
    Result of checking the theorem for one bridge instance.
    """

    theorem_name: str
    bridge: FiniteBridge
    hypothesis: TheoremHypothesis
    conclusion: TheoremConclusion
    status: TheoremStatus
    report: BridgeDistortionReport

    def implication_holds(self) -> bool:
        """
        Returns whether hypothesis implies conclusion.
        """

        if not self.hypothesis.holds():
            return True

        return self.conclusion.holds()

    def is_nonvacuous_verification(self) -> bool:
        """
        Returns whether this is a genuine instance where hypothesis and conclusion hold.
        """

        return (
            self.hypothesis.holds()
            and self.conclusion.holds()
            and self.status == TheoremStatus.VERIFIED_FOR_INSTANCE
        )

    def describe(self) -> str:
        """
        Returns a readable theorem check.
        """

        return (
            f"TheoremCheck: {self.theorem_name}\n"
            f"Bridge: {self.bridge.name}\n"
            f"Status: {self.status.value}\n"
            f"Implication holds: {self.implication_holds()}\n"
            f"Nonvacuous verification: {self.is_nonvacuous_verification()}\n"
            f"Hypothesis holds: {self.hypothesis.holds()}\n"
            f"Conclusion holds: {self.conclusion.holds()}"
        )


class BridgeDistortionTheorem:
    """
    Finite Bridge Distortion Theorem.

    Informal theorem:

    For a finite bridge B: U -> V, if B is total, U supports at least one
    semantic feature not supported by V, and some source statement requires
    such an absent feature, then B has at least one distorted translation.
    """

    name = "Finite Bridge Distortion Theorem"

    def check(self, bridge: FiniteBridge) -> TheoremCheck:
        """
        Checks the theorem for one bridge instance.
        """

        analyzer = DistortionAnalyzer()
        report = analyzer.analyze_bridge(bridge)

        hypothesis = TheoremHypothesis(
            bridge_is_total=bridge.is_total(),
            feature_mismatch_exists=bridge.has_feature_mismatch(),
            statement_uses_absent_feature=bool(
                bridge.statements_using_absent_features()
            ),
        )

        conclusion = TheoremConclusion(
            distortion_witness_exists=report.has_distortion(),
        )

        if hypothesis.holds() and conclusion.holds():
            status = TheoremStatus.VERIFIED_FOR_INSTANCE
        elif not hypothesis.holds():
            status = TheoremStatus.VACUOUSLY_TRUE_FOR_INSTANCE
        else:
            status = TheoremStatus.FAILED_FOR_INSTANCE

        return TheoremCheck(
            theorem_name=self.name,
            bridge=bridge,
            hypothesis=hypothesis,
            conclusion=conclusion,
            status=status,
            report=report,
        )

    def check_many(self, bridges: Tuple[FiniteBridge, ...]) -> Tuple[TheoremCheck, ...]:
        """
        Checks the theorem for many bridge instances.
        """

        return tuple(self.check(bridge) for bridge in bridges)

    def theorem_statement(self) -> str:
        """
        Returns the theorem statement in readable form.
        """

        return (
            "Finite Bridge Distortion Theorem:\n\n"
            "Let U and V be finite logical universes, and let B: U -> V be a "
            "finite bridge. Suppose:\n\n"
            "1. B is total on the statements of U.\n"
            "2. U supports at least one semantic feature not supported by V.\n"
            "3. At least one source statement in U requires such an absent feature.\n\n"
            "Then B has at least one distorted translation."
        )


if __name__ == "__main__":
    from src.rigor.bridge import collapse_bridge, identity_bridge
    from src.rigor.finite_universe import classical_finite_universe, modal_finite_universe

    theorem = BridgeDistortionTheorem()

    classical = classical_finite_universe()
    modal = modal_finite_universe()

    bridges = (
        identity_bridge(classical),
        collapse_bridge(
            name="Modal to Classical Collapse",
            source=modal,
            target=classical,
        ),
    )

    print(theorem.theorem_statement())

    for check in theorem.check_many(bridges):
        print()
        print(check.describe())
