"""
Tests for the Lean Lake project scaffold.
"""

from pathlib import Path


def test_lake_project_files_exist():
    root = Path("formal/aleph_omega_lake")

    assert (root / "lakefile.lean").exists()
    assert (root / "lean-toolchain").exists()
    assert (root / "AlephOmega.lean").exists()
    assert (root / "AlephOmega" / "AlephOmegaCore.lean").exists()


def test_lakefile_contains_package_and_library():
    text = Path("formal/aleph_omega_lake/lakefile.lean").read_text()

    assert "package" in text
    assert "lean_lib AlephOmega" in text


def test_lake_core_matches_main_lean_core():
    main = Path("formal/lean/AlephOmegaCore.lean").read_text()
    lake = Path("formal/aleph_omega_lake/AlephOmega/AlephOmegaCore.lean").read_text()

    assert "def AlephOmegaQuotientCategory" in lake
    assert "def TwoSystem" in lake
    assert len(lake) == len(main)


def test_lake_checker_script_exists():
    text = Path("scripts/check_lake.sh").read_text()

    assert "lake build" in text
    assert "formal/aleph_omega_lake" in text
