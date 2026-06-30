"""
Unit tests for Project ℵω bridge translation engine.

These tests verify that Phase 5 can:
- represent bridge maps,
- map symbols/features/truth values/proof statuses,
- translate statements between toy universes,
- produce translation results,
- compute distortion reports.
"""

from src.bridges.bridge_map import (
    BridgeKind,
    BridgeRisk,
    BridgeMap,
    FeatureMapping,
    SymbolMapping,
    identity_bridge,
    intuitionistic_to_classical_bridge,
    modal_to_classical_bridge,
    paraconsistent_to_classical_bridge,
    starter_bridge_maps,
)
from src.bridges.distortion import (
    DistortionAnalyzer,
    DistortionReport,
    TranslationGrade,
    rank_reports_by_distortion,
    rank_reports_by_quality,
)
from src.bridges.translation_result import (
    MeaningChange,
    MeaningChangeKind,
    TranslationResult,
    TranslationStatus,
)
from src.bridges.translator import UniverseTranslator
from src.toy_topoi.library import (
    classical_universe,
    find_universe_by_name,
    intuitionistic_universe,
    modal_universe,
    paraconsistent_universe,
)
from src.toy_topoi.statements import ProofStatus, starter_statements
from src.toy_topoi.truth_values import TruthValue


def test_symbol_mapping_loss_and_description():
    mapping = SymbolMapping(
        source_symbol="both",
        target_symbol=None,
        preserves_meaning=False,
        notes="Classical logic cannot preserve BOTH.",
    )

    assert mapping.is_loss()
    assert "both -> LOST" in mapping.describe()


def test_feature_mapping_loss_and_description():
    mapping = FeatureMapping(
        source_feature="contradiction_support",
        target_feature=None,
        preserves_feature=False,
    )

    assert mapping.is_loss()
    assert "contradiction_support -> LOST" in mapping.describe()


def test_identity_bridge_strength():
    bridge = identity_bridge("Test Universe")

    assert bridge.is_identity_bridge()
    assert bridge.kind == BridgeKind.IDENTITY
    assert bridge.risk == BridgeRisk.LOW
    assert bridge.bridge_strength_score() >= 9.0


def test_bridge_map_symbol_and_feature_defaults():
    bridge = BridgeMap(
        name="Test Bridge",
        source_universe_name="A",
        target_universe_name="B",
        kind=BridgeKind.GENERATED_EXPERIMENTAL,
    )

    assert bridge.map_symbol("forall") == "forall"
    assert bridge.map_feature("negation") == "negation"
    assert bridge.map_truth_value(TruthValue.TRUE) == TruthValue.TRUE
    assert bridge.map_proof_status(ProofStatus.UNTESTED) == ProofStatus.UNTESTED


def test_paraconsistent_to_classical_bridge_maps_contradiction():
    bridge = paraconsistent_to_classical_bridge(
        source_universe_name="Paraconsistent Contradiction-Tolerant Universe",
        target_universe_name="Classical Set-Theoretic Neighborhood",
    )

    assert bridge.kind == BridgeKind.CONTRADICTION_COLLAPSING
    assert bridge.map_symbol("both") is None
    assert bridge.map_feature("contradiction_support") is None
    assert bridge.map_truth_value(TruthValue.BOTH) == TruthValue.FALSE
    assert bridge.map_proof_status(ProofStatus.CONTRADICTORY) == ProofStatus.REFUTED
    assert bridge.bridge_strength_score() < 8.0


def test_modal_to_classical_bridge_maps_modal_truth():
    bridge = modal_to_classical_bridge(
        source_universe_name="Modal Possibility Universe",
        target_universe_name="Classical Set-Theoretic Neighborhood",
    )

    assert bridge.kind == BridgeKind.MODAL_FORGETFUL
    assert bridge.map_symbol("possible") is None
    assert bridge.map_truth_value(TruthValue.POSSIBLE) == TruthValue.TRUE
    assert bridge.map_truth_value(TruthValue.IMPOSSIBLE) == TruthValue.FALSE


def test_intuitionistic_to_classical_bridge_weakens_witness():
    bridge = intuitionistic_to_classical_bridge(
        source_universe_name="Intuitionistic Constructive Universe",
        target_universe_name="Classical Set-Theoretic Neighborhood",
    )

    assert bridge.kind == BridgeKind.CONSTRUCTIVE_TO_CLASSICAL
    assert bridge.map_symbol("witness") is None
    assert bridge.map_feature("constructive_evidence") == "existential_reasoning"


def test_starter_bridge_maps_load():
    bridges = starter_bridge_maps()

    assert len(bridges) >= 3
    assert all(isinstance(bridge, BridgeMap) for bridge in bridges)


def test_meaning_change_normalized_severity():
    change = MeaningChange(
        kind=MeaningChangeKind.SYMBOL_LOSS,
        description="Lost symbol.",
        severity=12.0,
    )

    assert change.normalized_severity() == 10.0
    assert "symbol_loss" in change.describe()


def test_universe_translator_returns_translation_result():
    translator = UniverseTranslator()

    bridge = paraconsistent_to_classical_bridge(
        source_universe_name="Paraconsistent Contradiction-Tolerant Universe",
        target_universe_name="Classical Set-Theoretic Neighborhood",
    )

    source_universe = paraconsistent_universe()
    target_universe = classical_universe()

    statement = [
        item for item in starter_statements()
        if item.origin_universe == "Paraconsistent Contradiction-Tolerant Universe"
    ][0]

    result = translator.translate(
        statement=statement,
        source_universe=source_universe,
        target_universe=target_universe,
        bridge=bridge,
    )

    assert isinstance(result, TranslationResult)
    assert result.source_statement.name == statement.name
    assert result.source_universe_name == source_universe.name
    assert result.target_universe_name == target_universe.name
    assert 0.0 <= result.translation_confidence <= 10.0
    assert 0.0 <= result.distortion_score() <= 10.0
    assert result.translation_status in set(TranslationStatus)


def test_translation_result_scores_and_summary():
    translator = UniverseTranslator()

    bridge = modal_to_classical_bridge(
        source_universe_name="Modal Possibility Universe",
        target_universe_name="Classical Set-Theoretic Neighborhood",
    )

    statement = [
        item for item in starter_statements()
        if item.origin_universe == "Modal Possibility Universe"
    ][0]

    result = translator.translate(
        statement=statement,
        source_universe=modal_universe(),
        target_universe=classical_universe(),
        bridge=bridge,
    )

    row = result.summary_row()

    assert "statement" in row
    assert "distortion" in row
    assert 0.0 <= result.symbol_preservation_score() <= 10.0
    assert 0.0 <= result.feature_preservation_score() <= 10.0
    assert 0.0 <= result.average_meaning_change_severity() <= 10.0
    assert isinstance(result.is_high_quality_translation(), bool)


def test_distortion_analyzer_returns_report():
    translator = UniverseTranslator()
    analyzer = DistortionAnalyzer()

    bridge = intuitionistic_to_classical_bridge(
        source_universe_name="Intuitionistic Constructive Universe",
        target_universe_name="Classical Set-Theoretic Neighborhood",
    )

    statement = [
        item for item in starter_statements()
        if item.origin_universe == "Intuitionistic Constructive Universe"
    ][0]

    result = translator.translate(
        statement=statement,
        source_universe=intuitionistic_universe(),
        target_universe=classical_universe(),
        bridge=bridge,
    )

    report = analyzer.analyze(result)

    assert isinstance(report, DistortionReport)
    assert report.statement_name == statement.name
    assert 0.0 <= report.overall_distortion_index <= 10.0
    assert report.translation_grade in set(TranslationGrade)
    assert "overall_distortion_index" in report.as_dict()


def test_distortion_ranking_helpers():
    translator = UniverseTranslator()
    analyzer = DistortionAnalyzer()

    results = []

    for bridge in starter_bridge_maps():
        source_universe = find_universe_by_name(bridge.source_universe_name)
        target_universe = find_universe_by_name(bridge.target_universe_name)

        assert source_universe is not None
        assert target_universe is not None

        for statement in starter_statements():
            if statement.origin_universe == bridge.source_universe_name:
                results.append(
                    translator.translate(
                        statement=statement,
                        source_universe=source_universe,
                        target_universe=target_universe,
                        bridge=bridge,
                    )
                )

    reports = analyzer.analyze_many(results)

    assert len(reports) == len(results)

    by_distortion = rank_reports_by_distortion(reports)
    by_quality = rank_reports_by_quality(reports)

    assert len(by_distortion) == len(reports)
    assert len(by_quality) == len(reports)

    if len(reports) >= 2:
        assert by_distortion[0].overall_distortion_index >= by_distortion[-1].overall_distortion_index
        assert by_quality[0].overall_distortion_index <= by_quality[-1].overall_distortion_index
