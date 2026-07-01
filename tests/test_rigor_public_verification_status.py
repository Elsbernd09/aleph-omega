"""
Tests for public verification status generation.
"""

from pathlib import Path

from src.rigor.public_verification_status import (
    PublicVerificationStatus,
    PublicVerificationStatusBuilder,
    VerificationItem,
)


def test_public_verification_status_builds():
    status = PublicVerificationStatusBuilder().build()

    assert isinstance(status, PublicVerificationStatus)
    assert status.item_count() >= 10
    assert len(status.lean_checked_items()) >= 5
    assert len(status.python_tested_items()) >= 2
    assert len(status.ci_checked_items()) >= 2
    assert "PublicVerificationStatus" in status.describe()


def test_verification_item_describe():
    status = PublicVerificationStatusBuilder().build()
    item = status.items[0]

    assert isinstance(item, VerificationItem)
    assert "VerificationItem" in item.describe()


def test_public_verification_status_markdown_contains_core_claims():
    status = PublicVerificationStatusBuilder().build()
    markdown = PublicVerificationStatusBuilder().to_markdown(status)

    assert "# Project Aleph-Omega Verification Status" in markdown
    assert "Lean-checked" in markdown
    assert "Python-tested" in markdown
    assert "CI-checked" in markdown
    assert "./scripts/check_formal_stack.sh" in markdown
    assert "Universal institution theorem" in markdown
    assert "explicitly not claimed" in markdown


def test_public_verification_status_write_markdown(tmp_path):
    status = PublicVerificationStatusBuilder().build()
    output_path = tmp_path / "verification_status.md"

    written = PublicVerificationStatusBuilder().write_markdown(
        status=status,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Verification Status" in written.read_text()
