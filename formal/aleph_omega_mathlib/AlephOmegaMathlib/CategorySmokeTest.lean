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

namespace AlephOmegaMathlib

open CategoryTheory

/-
Phase 29C: First real Mathlib Category instance.

This is a smoke-test category instance for SmokeObject.

Objects:
- SmokeObject

Morphisms:
- functions between carriers

Identity:
- identity function

Composition:
- function composition

This confirms that the experimental Mathlib project can define an actual
Mathlib Category instance.
-/

instance smokeCategory : Category SmokeObject where
  Hom A B := SmokeHom A B
  id A := SmokeId A
  comp f g := SmokeComp f g
  id_comp := by
    intro X Y f
    rfl
  comp_id := by
    intro X Y f
    rfl
  assoc := by
    intro W X Y Z f g h
    rfl

theorem smoke_category_id_is_smoke_id (A : SmokeObject) :
  CategoryStruct.id A = SmokeId A := by
    rfl

theorem smoke_category_comp_is_smoke_comp
  {A B C : SmokeObject} (f : A ⟶ B) (g : B ⟶ C) :
  f ≫ g = SmokeComp f g := by
    rfl

theorem smoke_category_left_identity
  {A B : SmokeObject} (f : A ⟶ B) :
  𝟙 A ≫ f = f := by
    simp

theorem smoke_category_right_identity
  {A B : SmokeObject} (f : A ⟶ B) :
  f ≫ 𝟙 B = f := by
    simp

theorem smoke_category_assoc
  {A B C D : SmokeObject}
  (f : A ⟶ B) (g : B ⟶ C) (h : C ⟶ D) :
  (f ≫ g) ≫ h = f ≫ (g ≫ h) := by
    simp

end AlephOmegaMathlib
