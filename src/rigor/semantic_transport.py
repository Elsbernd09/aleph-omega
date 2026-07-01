"""
Semantic transport along finite bridges.

This module defines how an interpretation on a source universe can be transported
along a finite bridge to produce an interpretation on a target universe.

This is a finite toy model of semantic transport:
- source statements have truth values;
- a bridge maps source statements to target statements;
- transported truth values are assigned to target statements.

If multiple source statements map to the same target statement, conflicts may
occur. The transport report records these conflicts.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Tuple

from src.rigor.bridge import FiniteBridge
from src.rigor.finite_universe import FiniteStatement
from src.rigor.interpretation import UniverseInterpretation
from src.rigor.semantics import FiniteTruthValue, FiniteTruthValueSpace


class TransportStatus(str, Enum):
    """
    Status of semantic transport.
    """

    SUCCESS = "success"
    PARTIAL = "partial"
    CONFLICT = "conflict"
    EMPTY = "empty"


@dataclass(frozen=True)
class TransportConflict:
    """
    Conflict caused by assigning different truth values to the same target statement.
    """

    target_statement: FiniteStatement
    existing_value: FiniteTruthValue
    incoming_value: FiniteTruthValue
    source_statement: FiniteStatement

    def describe(self) -> str:
        """
        Returns a readable conflict description.
        """

        return (
            f"TransportConflict\n"
            f"Target statement: {self.target_statement.name}\n"
            f"Existing value: {self.existing_value.value}\n"
            f"Incoming value: {self.incoming_value.value}\n"
            f"Incoming source statement: {self.source_statement.name}"
        )


@dataclass(frozen=True)
class SemanticTransportReport:
    """
    Report for transporting an interpretation along a bridge.
    """

    bridge: FiniteBridge
    source_interpretation: UniverseInterpretation
    target_truth_space: FiniteTruthValueSpace
    transported_interpretation: UniverseInterpretation
    status: TransportStatus
    transported_count: int
    undefined_count: int
    conflicts: Tuple[TransportConflict, ...] = field(default_factory=tuple)

    def has_conflicts(self) -> bool:
        """
        Returns whether transport had conflicts.
        """

        return bool(self.conflicts)

    def is_successful(self) -> bool:
        """
        Returns whether transport succeeded without undefined translations or conflicts.
        """

        return self.status == TransportStatus.SUCCESS

    def describe(self) -> str:
        """
        Returns a readable transport report.
        """

        return (
            f"SemanticTransportReport\n"
            f"Bridge: {self.bridge.name}\n"
            f"Source universe: {self.bridge.source.name}\n"
            f"Target universe: {self.bridge.target.name}\n"
            f"Target truth space: {self.target_truth_space.name}\n"
            f"Status: {self.status.value}\n"
            f"Transported count: {self.transported_count}\n"
            f"Undefined count: {self.undefined_count}\n"
            f"Conflict count: {len(self.conflicts)}"
        )


class SemanticTransporter:
    """
    Transports interpretations along finite bridges.
    """

    def transport(
        self,
        bridge: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        target_truth_space: FiniteTruthValueSpace,
    ) -> SemanticTransportReport:
        """
        Transports a source interpretation along a bridge.

        Only assigned source statements can transport truth values.

        If bridge(s) is undefined, no target value is assigned for s.
        If two source statements assign different values to the same target statement,
        a conflict is recorded and the first assignment is retained.
        """

        target_assignment: Dict[FiniteStatement, FiniteTruthValue] = {}
        conflicts = []
        transported_count = 0
        undefined_count = 0

        for source_statement in sorted(
            bridge.source.statements,
            key=lambda item: item.name,
        ):
            source_value: Optional[FiniteTruthValue] = (
                source_interpretation.assignment.get(source_statement)
            )

            if source_value is None:
                continue

            translation = bridge.translate(source_statement)

            if translation.target_statement is None:
                undefined_count += 1
                continue

            target_statement = translation.target_statement

            if target_statement in target_assignment:
                existing_value = target_assignment[target_statement]

                if existing_value != source_value:
                    conflicts.append(
                        TransportConflict(
                            target_statement=target_statement,
                            existing_value=existing_value,
                            incoming_value=source_value,
                            source_statement=source_statement,
                        )
                    )
                continue

            target_assignment[target_statement] = source_value
            transported_count += 1

        transported_interpretation = UniverseInterpretation(
            universe=bridge.target,
            truth_space=target_truth_space,
            assignment=target_assignment,
            description=f"Transported along bridge {bridge.name}.",
        )

        if conflicts:
            status = TransportStatus.CONFLICT
        elif transported_count == 0 and undefined_count == 0:
            status = TransportStatus.EMPTY
        elif undefined_count > 0:
            status = TransportStatus.PARTIAL
        else:
            status = TransportStatus.SUCCESS

        return SemanticTransportReport(
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_truth_space=target_truth_space,
            transported_interpretation=transported_interpretation,
            status=status,
            transported_count=transported_count,
            undefined_count=undefined_count,
            conflicts=tuple(conflicts),
        )


if __name__ == "__main__":
    from src.rigor.bridge import identity_bridge
    from src.rigor.finite_universe import classical_finite_universe
    from src.rigor.interpretation import constant_interpretation
    from src.rigor.semantics import FiniteTruthValue, classical_truth_space

    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge = identity_bridge(universe)

    report = SemanticTransporter().transport(
        bridge=bridge,
        source_interpretation=interpretation,
        target_truth_space=truth_space,
    )

    print(report.describe())
