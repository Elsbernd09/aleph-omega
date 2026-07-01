"""
Tests for Lake synchronization guard scripts.
"""

from pathlib import Path


def test_sync_scripts_exist():
    assert Path("scripts/sync_lake_core.sh").exists()
    assert Path("scripts/check_lake_sync.sh").exists()


def test_sync_script_copies_main_core_to_lake_core():
    text = Path("scripts/sync_lake_core.sh").read_text()

    assert "formal/lean/AlephOmegaCore.lean" in text
    assert "formal/aleph_omega_lake/AlephOmega/AlephOmegaCore.lean" in text
    assert "cp" in text


def test_sync_check_uses_cmp():
    text = Path("scripts/check_lake_sync.sh").read_text()

    assert "cmp -s" in text
    assert "Lean core files are synchronized" in text
    assert "out of sync" in text


def test_lake_checker_calls_sync_checker():
    text = Path("scripts/check_lake.sh").read_text()

    assert "./scripts/check_lake_sync.sh" in text
    assert "lake build" in text
