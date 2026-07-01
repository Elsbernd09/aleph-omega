"""
Identity laws for finite universe categories.

For a bridge f: A -> B, the identity laws say:

1. Left identity:
   f ∘ id_A = f

2. Right identity:
   id_B ∘ f = f

In the composition convention used by this project:

compose_bridges(first, second) means second ∘ first.

So:

- left identity is compose_bridges(id_A, f)
- right identity is compose_bridges(f, id_B)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.category import FiniteUniverseCategory
from src.rigor.composition import compose_bridges, same_bridge_mapping


class IdentityLawStatus(str, Enum):
    """
    Status of an identity law check.
    """

    HOLDS = "holds"
    FAILS_LEFT_IDENTITY = "fails_left_identity"
    FAILS_RIGHT_IDENTITY = "fails_right_identity"
    FAILS_BOTH = "fails_both"


@dataclass(frozen=True)
class IdentityLawCheck:
    """
    Identity law check for one bridge.
    """

    bridge: FiniteBridge
    left_identity_composite: FiniteBridge
    right_identity_composite: FiniteBridge
    left_identity_holds: bool
    right_identity_holds: bool
    status: IdentityLawStatus

    def holds(self) -> bool:
        """
        Returns whether both identity laws hold.
        """

        return self.left_identity_holds and self.right_identity_holds

    def describe(self) -> str:
        """
        Returns a readable identity law check.
        """

        return (
            f"IdentityLawCheck\n"
            f"Bridge: {self.bridge.name}\n"
            f"Left identity holds: {self.left_identity_holds}\n"
            f"Right identity holds: {self.right_identity_holds}\n"
            f"Status: {self.status.value}"
        )


@dataclass(frozen=True)
class IdentityLawReport:
    """
    Identity law report for a finite universe category.
    """

    category: FiniteUniverseCategory
    checks: Tuple[IdentityLawCheck, ...]

    def holds(self) -> bool:
        """
        Returns whether identity laws hold for all checked morphisms.
        """

        return all(check.holds() for check in self.checks)

    def failing_checks(self) -> Tuple[IdentityLawCheck, ...]:
        """
        Returns identity law checks that failed.
        """

        return tuple(check for check in self.checks if not check.holds())

    def success_count(self) -> int:
        """
        Counts successful checks.
        """

        return sum(1 for check in self.checks if check.holds())

    def failure_count(self) -> int:
        """
        Counts failed checks.
        """

        return len(self.failing_checks())

    def describe(self) -> str:
        """
        Returns a readable identity law report.
        """

        return (
            f"IdentityLawReport\n"
            f"Category: {self.category.name}\n"
            f"Check count: {len(self.checks)}\n"
            f"Success count: {self.success_count()}\n"
            f"Failure count: {self.failure_count()}\n"
            f"Identity laws hold: {self.holds()}"
        )


class IdentityLawAnalyzer:
    """
    Analyzer for identity laws.
    """

    def check_bridge(self, bridge: FiniteBridge) -> IdentityLawCheck:
        """
        Checks left and right identity laws for one bridge f: A -> B.
        """

        left_identity = identity_bridge(bridge.source)
        right_identity = identity_bridge(bridge.target)

        left_result = compose_bridges(left_identity, bridge)
        right_result = compose_bridges(bridge, right_identity)

        left_composite = left_result.composite
        right_composite = right_result.composite

        left_holds = (
            left_composite is not None
            and same_bridge_mapping(left_composite, bridge)
        )

        right_holds = (
            right_composite is not None
            and same_bridge_mapping(right_composite, bridge)
        )

        if left_holds and right_holds:
            status = IdentityLawStatus.HOLDS
        elif not left_holds and not right_holds:
            status = IdentityLawStatus.FAILS_BOTH
        elif not left_holds:
            status = IdentityLawStatus.FAILS_LEFT_IDENTITY
        else:
            status = IdentityLawStatus.FAILS_RIGHT_IDENTITY

        if left_composite is None:
            left_composite = FiniteBridge(
                name="Undefined Left Identity Composite",
                source=bridge.source,
                target=bridge.target,
                mapping={},
                description="Left identity composite was undefined.",
            )

        if right_composite is None:
            right_composite = FiniteBridge(
                name="Undefined Right Identity Composite",
                source=bridge.source,
                target=bridge.target,
                mapping={},
                description="Right identity composite was undefined.",
            )

        return IdentityLawCheck(
            bridge=bridge,
            left_identity_composite=left_composite,
            right_identity_composite=right_composite,
            left_identity_holds=left_holds,
            right_identity_holds=right_holds,
            status=status,
        )

    def check_category(self, category: FiniteUniverseCategory) -> IdentityLawReport:
        """
        Checks identity laws for every morphism in a category.
        """

        checks = tuple(
            self.check_bridge(bridge)
            for bridge in sorted(category.morphisms, key=lambda item: item.name)
        )

        return IdentityLawReport(
            category=category,
            checks=checks,
        )


if __name__ == "__main__":
    from src.rigor.category import starter_finite_universe_category

    category = starter_finite_universe_category()
    report = IdentityLawAnalyzer().check_category(category)

    print(report.describe())

    for check in report.checks:
        print()
        print(check.describe())
