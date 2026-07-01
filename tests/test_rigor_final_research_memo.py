"""
Tests for final research memo generation.
"""

from pathlib import Path

from src.rigor.final_research_memo import FinalResearchMemo, FinalResearchMemoBuilder


def test_final_research_memo_builds():
    memo = FinalResearchMemoBuilder().build()

    assert isinstance(memo, FinalResearchMemo)
    assert "Project Aleph-Omega" in memo.title
    assert memo.section_count() >= 8
    assert memo.word_count() > 300
    assert "FinalResearchMemo" in memo.describe()


def test_final_research_memo_markdown_contains_sections():
    memo = FinalResearchMemoBuilder().build()
    markdown = memo.to_markdown()

    assert "# Project Aleph-Omega Final Research Memo" in markdown
    assert "## Abstract" in markdown
    assert "## Architecture Summary" in markdown
    assert "## Correct Research Claim" in markdown
    assert "## Future Work" in markdown


def test_final_research_memo_write_markdown(tmp_path):
    memo = FinalResearchMemoBuilder().build()
    output_path = tmp_path / "final_research_memo.md"

    written = FinalResearchMemoBuilder().write_markdown(
        memo=memo,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Project Aleph-Omega Final Research Memo" in written.read_text()
