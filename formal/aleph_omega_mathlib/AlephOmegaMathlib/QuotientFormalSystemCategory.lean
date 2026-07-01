import AlephOmegaMathlib.FormalSystemCategory

namespace AlephOmegaMathlib

open CategoryTheory

/-
Phase 30B: Mathlib quotient category prototype.

This file creates a real Mathlib Category instance whose morphisms are quotient
classes of satisfaction-preserving morphisms.

To avoid conflicting with the direct category instance on FormalSystem, we use a
wrapper object type:

  QuotientFormalSystem

Objects:
- QuotientFormalSystem

Morphisms:
- quotient classes of PreservationMorphism

Identity:
- quotient class of identityPreservation

Composition:
- quotient class of composePreservation

This is a prototype quotient category inside Mathlib infrastructure.
-/

universe u v

/--
Two preservation morphisms are equivalent if they have the same sentence
translation and the same model map.

The preservation proof field is intentionally ignored.
-/
def PreservationEquivalent
  {A B : FormalSystem.{u, v}}
  (F G : PreservationMorphism A B) : Prop :=
  (∀ φ : A.Sentence, F.translate φ = G.translate φ) ∧
  (∀ m : A.Model, F.mapModel m = G.mapModel m)

/--
Reflexivity of preservation-morphism equivalence.
-/
theorem preservation_equiv_refl
  {A B : FormalSystem.{u, v}}
  (F : PreservationMorphism A B) :
  PreservationEquivalent F F := by
    constructor
    · intro φ
      rfl
    · intro m
      rfl

/--
Symmetry of preservation-morphism equivalence.
-/
theorem preservation_equiv_symm
  {A B : FormalSystem.{u, v}}
  {F G : PreservationMorphism A B} :
  PreservationEquivalent F G ->
  PreservationEquivalent G F := by
    intro h
    constructor
    · intro φ
      exact Eq.symm (h.1 φ)
    · intro m
      exact Eq.symm (h.2 m)

/--
Transitivity of preservation-morphism equivalence.
-/
theorem preservation_equiv_trans
  {A B : FormalSystem.{u, v}}
  {F G H : PreservationMorphism A B} :
  PreservationEquivalent F G ->
  PreservationEquivalent G H ->
  PreservationEquivalent F H := by
    intro hFG hGH
    constructor
    · intro φ
      exact Eq.trans (hFG.1 φ) (hGH.1 φ)
    · intro m
      exact Eq.trans (hFG.2 m) (hGH.2 m)

/--
Setoid on preservation morphisms.
-/
instance preservationSetoid
  (A B : FormalSystem.{u, v}) :
  Setoid (PreservationMorphism A B) where
    r := PreservationEquivalent
    iseqv := {
      refl := by
        intro F
        exact preservation_equiv_refl F
      symm := by
        intro F G h
        exact preservation_equiv_symm h
      trans := by
        intro F G H hFG hGH
        exact preservation_equiv_trans hFG hGH
    }

/--
Quotient hom type between formal systems.
-/
def QuotientPreservationHom
  (A B : FormalSystem.{u, v}) : Type (max u v) :=
  Quotient (preservationSetoid A B)

/--
Quotient class of a preservation morphism.
-/
def quotientPreservationOf
  {A B : FormalSystem.{u, v}}
  (F : PreservationMorphism A B) :
  QuotientPreservationHom A B :=
  Quotient.mk (preservationSetoid A B) F

/--
Quotient identity morphism.
-/
def quotientIdentityPreservation
  (A : FormalSystem.{u, v}) :
  QuotientPreservationHom A A :=
  quotientPreservationOf (identityPreservation A)

/--
Composition respects preservation-morphism equivalence.
-/
theorem compose_preservation_respects_equivalence
  {A B C : FormalSystem.{u, v}}
  {F F' : PreservationMorphism A B}
  {G G' : PreservationMorphism B C} :
  PreservationEquivalent F F' ->
  PreservationEquivalent G G' ->
  PreservationEquivalent
    (composePreservation F G)
    (composePreservation F' G') := by
      intro hF hG
      constructor
      · intro φ
        calc
          (composePreservation F G).translate φ
              = G.translate (F.translate φ) := rfl
          _ = G.translate (F'.translate φ) := by rw [hF.1 φ]
          _ = G'.translate (F'.translate φ) := hG.1 (F'.translate φ)
          _ = (composePreservation F' G').translate φ := rfl
      · intro m
        calc
          (composePreservation F G).mapModel m
              = G.mapModel (F.mapModel m) := rfl
          _ = G.mapModel (F'.mapModel m) := by rw [hF.2 m]
          _ = G'.mapModel (F'.mapModel m) := hG.2 (F'.mapModel m)
          _ = (composePreservation F' G').mapModel m := rfl

/--
Composition of quotient preservation morphisms.
-/
def quotientComposePreservation
  {A B C : FormalSystem.{u, v}}
  (qF : QuotientPreservationHom A B)
  (qG : QuotientPreservationHom B C) :
  QuotientPreservationHom A C :=
  Quotient.liftOn₂
    qF
    qG
    (fun F G => quotientPreservationOf (composePreservation F G))
    (by
      intro F F' G G' hF hG
      apply Quotient.sound
      exact compose_preservation_respects_equivalence hF hG)

/--
Wrapper object type for the quotient category.

This avoids conflicting with the direct Mathlib category instance on FormalSystem.
-/
structure QuotientFormalSystem where
  system : FormalSystem.{u, v}

/--
Hom type for quotient formal systems.
-/
abbrev QuotientFormalSystemHom
  (A B : QuotientFormalSystem.{u, v}) : Type (max u v) :=
  QuotientPreservationHom A.system B.system

/--
Real Mathlib Category instance for quotient formal systems.
-/
instance quotientFormalSystemCategory :
  Category (QuotientFormalSystem.{u, v}) where
    Hom A B := QuotientFormalSystemHom A B
    id A := quotientIdentityPreservation A.system
    comp qF qG := quotientComposePreservation qF qG
    id_comp := by
      intro A B qF
      refine Quotient.inductionOn qF ?_
      intro F
      apply Quotient.sound
      constructor
      · intro φ
        rfl
      · intro m
        rfl
    comp_id := by
      intro A B qF
      refine Quotient.inductionOn qF ?_
      intro F
      apply Quotient.sound
      constructor
      · intro φ
        rfl
      · intro m
        rfl
    assoc := by
      intro A B C D qF qG qH
      refine Quotient.inductionOn qF ?_
      intro F
      refine Quotient.inductionOn qG ?_
      intro G
      refine Quotient.inductionOn qH ?_
      intro H
      apply Quotient.sound
      constructor
      · intro φ
        rfl
      · intro m
        rfl

/--
Boolean object for the quotient category.
-/
def QuotientBoolFormalSystem : QuotientFormalSystem where
  system := BoolFormalSystem

/--
The quotient category identity on the Boolean object composes with itself.
-/
theorem quotient_bool_identity_composes :
  (𝟙 QuotientBoolFormalSystem : QuotientBoolFormalSystem ⟶ QuotientBoolFormalSystem) ≫
  (𝟙 QuotientBoolFormalSystem : QuotientBoolFormalSystem ⟶ QuotientBoolFormalSystem)
  =
  (𝟙 QuotientBoolFormalSystem : QuotientBoolFormalSystem ⟶ QuotientBoolFormalSystem) := by
    simp

end AlephOmegaMathlib
