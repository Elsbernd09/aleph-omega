import Mathlib.CategoryTheory.Category.Basic

namespace AlephOmegaMathlib

open CategoryTheory

/-
Phase 29D: Mathlib category for satisfaction-preserving morphisms.

This file defines a real Mathlib Category instance where:

Objects:
- FormalSystem

Morphisms:
- PreservationMorphism A B

Identity:
- identityPreservation

Composition:
- composePreservation

This is not yet the quotient category. It is the direct preservation-morphism
category.
-/

universe u v

/--
A formal system consists of models, sentences, and a satisfaction relation.
-/
structure FormalSystem where
  Model : Type u
  Sentence : Type v
  Sat : Model -> Sentence -> Prop

/--
A satisfaction-preserving morphism between formal systems.
-/
structure PreservationMorphism (A B : FormalSystem.{u, v}) where
  translate : A.Sentence -> B.Sentence
  mapModel : A.Model -> B.Model
  preserves :
    ∀ (m : A.Model) (φ : A.Sentence),
      A.Sat m φ ->
      B.Sat (mapModel m) (translate φ)

/--
Identity preservation morphism.
-/
def identityPreservation (A : FormalSystem.{u, v}) :
  PreservationMorphism A A where
    translate := fun φ => φ
    mapModel := fun m => m
    preserves := by
      intro m φ h
      exact h

/--
Composition of preservation morphisms.
-/
def composePreservation
  {A B C : FormalSystem.{u, v}}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C) :
  PreservationMorphism A C where
    translate := fun φ => G.translate (F.translate φ)
    mapModel := fun m => G.mapModel (F.mapModel m)
    preserves := by
      intro m φ h
      exact G.preserves (F.mapModel m) (F.translate φ) (F.preserves m φ h)

/--
A real Mathlib Category instance for formal systems and satisfaction-preserving
morphisms.
-/
instance formalSystemCategory : Category (FormalSystem.{u, v}) where
  Hom A B := PreservationMorphism A B
  id A := identityPreservation A
  comp F G := composePreservation F G
  id_comp := by
    intro A B F
    cases F
    rfl
  comp_id := by
    intro A B F
    cases F
    rfl
  assoc := by
    intro A B C D F G H
    cases F
    cases G
    cases H
    rfl

/--
The Mathlib category identity agrees with identityPreservation.
-/
theorem formal_category_id_is_identity
  (A : FormalSystem.{u, v}) :
  (𝟙 A : A ⟶ A) = identityPreservation A := by
    rfl

/--
The Mathlib category composition agrees with composePreservation.
-/
theorem formal_category_comp_is_compose
  {A B C : FormalSystem.{u, v}}
  (F : A ⟶ B)
  (G : B ⟶ C) :
  F ≫ G = composePreservation F G := by
    rfl

/--
A concrete Boolean formal system.
-/
def BoolFormalSystem : FormalSystem where
  Model := Bool
  Sentence := Bool
  Sat := fun m φ => m = φ

/--
The identity morphism in the Mathlib category preserves true satisfaction in
BoolFormalSystem.
-/
theorem bool_formal_category_identity_preserves_true :
  BoolFormalSystem.Sat
    (((𝟙 BoolFormalSystem : BoolFormalSystem ⟶ BoolFormalSystem).mapModel true))
    (((𝟙 BoolFormalSystem : BoolFormalSystem ⟶ BoolFormalSystem).translate true)) := by
      rfl

/--
The identity morphism in the Mathlib category preserves false satisfaction in
BoolFormalSystem.
-/
theorem bool_formal_category_identity_preserves_false :
  BoolFormalSystem.Sat
    (((𝟙 BoolFormalSystem : BoolFormalSystem ⟶ BoolFormalSystem).mapModel false))
    (((𝟙 BoolFormalSystem : BoolFormalSystem ⟶ BoolFormalSystem).translate false)) := by
      rfl

end AlephOmegaMathlib
