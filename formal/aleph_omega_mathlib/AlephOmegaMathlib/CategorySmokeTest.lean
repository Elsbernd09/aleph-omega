import Mathlib.CategoryTheory.Category.Basic

namespace AlephOmegaMathlib

/-
Phase 29B: Mathlib smoke test.

This file intentionally does not import the full Aleph-Omega core yet.

Its job is only to verify that the experimental Mathlib Lake project can import
Mathlib's basic category-theory definitions.
-/

universe u

structure SmokeObject where
  carrier : Type u

def SmokeHom (A B : SmokeObject) : Type u :=
  A.carrier -> B.carrier

def SmokeId (A : SmokeObject) : SmokeHom A A :=
  fun x => x

def SmokeComp {A B C : SmokeObject} :
  SmokeHom A B -> SmokeHom B C -> SmokeHom A C :=
  fun f g => g ∘ f

theorem smoke_left_identity {A B : SmokeObject} (f : SmokeHom A B) :
  SmokeComp (SmokeId A) f = f := by
    rfl

theorem smoke_right_identity {A B : SmokeObject} (f : SmokeHom A B) :
  SmokeComp f (SmokeId B) = f := by
    rfl

theorem smoke_associativity {A B C D : SmokeObject}
  (f : SmokeHom A B) (g : SmokeHom B C) (h : SmokeHom C D) :
  SmokeComp (SmokeComp f g) h = SmokeComp f (SmokeComp g h) := by
    rfl

end AlephOmegaMathlib
