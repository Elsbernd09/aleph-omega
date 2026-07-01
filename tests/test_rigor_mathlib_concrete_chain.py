"""
Tests for Mathlib concrete three-system chain.
"""

from pathlib import Path


def test_mathlib_concrete_chain_file_exists():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/ConcreteChain.lean")

    assert path.exists()


def test_mathlib_concrete_systems_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/ConcreteChain.lean").read_text()

    assert "def MathlibTwoSystem" in text
    assert "def MathlibRenamedSystem" in text
    assert "def MathlibThirdSystem" in text


def test_mathlib_concrete_morphisms_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/ConcreteChain.lean").read_text()

    assert "def mathlibTwoToRenamedMorphism" in text
    assert "def mathlibRenamedToThirdMorphism" in text
    assert "def mathlibTwoToThirdComposite" in text


def test_mathlib_concrete_quotient_chain_exists():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/ConcreteChain.lean").read_text()

    assert "def qMathlibTwoToRenamed" in text
    assert "def qMathlibRenamedToThird" in text
    assert "def qMathlibTwoToThird" in text
    assert "theorem q_mathlib_concrete_chain_composes" in text
    assert "theorem q_category_mathlib_concrete_chain_composes" in text


def test_mathlib_entry_imports_concrete_chain():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib.lean").read_text()

    assert "import AlephOmegaMathlib.ConcreteChain" in text


def test_mathlib_concrete_chain_docs_exist():
    text = Path("docs/mathlib_concrete_chain.md").read_text()

    assert "Mathlib Concrete Three-System Chain" in text
    assert "q_category_mathlib_concrete_chain_composes" in text
    assert "experimental Mathlib quotient-category track" in text
