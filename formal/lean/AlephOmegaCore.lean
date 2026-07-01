/-
Project Aleph-Omega: Lean Core Formalization Prototype

This file formalizes the smallest serious mathematical core of the
finite institution-like layer.

It defines:

1. A system with models, sentences, and satisfaction.
2. A satisfaction-preserving morphism.
3. The identity morphism.
4. Composition of satisfaction-preserving morphisms.

The key theorem-like content is that preservation is closed under composition.
-/

namespace AlephOmega

/--
A formal system consists of:

- a type of models,
- a type of sentences,
- a satisfaction relation between models and sentences.

This is intentionally minimal. It captures the core mathematical pattern behind
the finite institution-like layer of Project Aleph-Omega.
-/
structure FormalSystem where
  Model : Type
  Sentence : Type
  Sat : Model -> Sentence -> Prop

/--
A satisfaction-preserving morphism from system A to system B consists of:

- a translation from A-sentences to B-sentences,
- a map from A-models to B-models,
- a proof that satisfaction is preserved.

If a model m satisfies a sentence φ in A, then the mapped model satisfies the
translated sentence in B.
-/
structure PreservationMorphism (A B : FormalSystem) where
  translate : A.Sentence -> B.Sentence
  mapModel : A.Model -> B.Model
  preserves :
    ∀ (m : A.Model) (φ : A.Sentence),
      A.Sat m φ -> B.Sat (mapModel m) (translate φ)

/--
The identity morphism preserves satisfaction.

This is the first basic category-style law.
-/
def identityMorphism (A : FormalSystem) : PreservationMorphism A A where
  translate := fun φ => φ
  mapModel := fun m => m
  preserves := by
    intro m φ h
    exact h

/--
The composition of two satisfaction-preserving morphisms preserves satisfaction.

If F : A -> B preserves satisfaction and G : B -> C preserves satisfaction,
then G ∘ F : A -> C also preserves satisfaction.
-/
def composeMorphism
  {A B C : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C) :
  PreservationMorphism A C where
  translate := fun φ => G.translate (F.translate φ)
  mapModel := fun m => G.mapModel (F.mapModel m)
  preserves := by
    intro m φ h
    exact G.preserves (F.mapModel m) (F.translate φ) (F.preserves m φ h)

/--
Explicit theorem statement:

Composition preserves satisfaction.
-/
theorem composition_preserves_satisfaction
  {A B C : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C)
  (m : A.Model)
  (φ : A.Sentence)
  (h : A.Sat m φ) :
  C.Sat ((composeMorphism F G).mapModel m) ((composeMorphism F G).translate φ) := by
    exact (composeMorphism F G).preserves m φ h

/--
Explicit theorem statement:

Identity preserves satisfaction.
-/
theorem identity_preserves_satisfaction
  (A : FormalSystem)
  (m : A.Model)
  (φ : A.Sentence)
  (h : A.Sat m φ) :
  A.Sat ((identityMorphism A).mapModel m) ((identityMorphism A).translate φ) := by
    exact h

end AlephOmega

namespace AlephOmega

/--
Left identity law for preservation morphisms.

The identity morphism composed before F has the same sentence translation and
model map as F.
-/
theorem left_identity_translation
  {A B : FormalSystem}
  (F : PreservationMorphism A B)
  (φ : A.Sentence) :
  (composeMorphism (identityMorphism A) F).translate φ = F.translate φ := by
    rfl

theorem left_identity_model_map
  {A B : FormalSystem}
  (F : PreservationMorphism A B)
  (m : A.Model) :
  (composeMorphism (identityMorphism A) F).mapModel m = F.mapModel m := by
    rfl

/--
Right identity law for preservation morphisms.

F composed before the identity morphism has the same sentence translation and
model map as F.
-/
theorem right_identity_translation
  {A B : FormalSystem}
  (F : PreservationMorphism A B)
  (φ : A.Sentence) :
  (composeMorphism F (identityMorphism B)).translate φ = F.translate φ := by
    rfl

theorem right_identity_model_map
  {A B : FormalSystem}
  (F : PreservationMorphism A B)
  (m : A.Model) :
  (composeMorphism F (identityMorphism B)).mapModel m = F.mapModel m := by
    rfl

/--
Associativity law for sentence translation.

For F : A -> B, G : B -> C, and H : C -> D, the sentence translation part of
composition is associative.
-/
theorem associativity_translation
  {A B C D : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C)
  (H : PreservationMorphism C D)
  (φ : A.Sentence) :
  (composeMorphism (composeMorphism F G) H).translate φ =
  (composeMorphism F (composeMorphism G H)).translate φ := by
    rfl

/--
Associativity law for model maps.

For F : A -> B, G : B -> C, and H : C -> D, the model-map part of composition
is associative.
-/
theorem associativity_model_map
  {A B C D : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C)
  (H : PreservationMorphism C D)
  (m : A.Model) :
  (composeMorphism (composeMorphism F G) H).mapModel m =
  (composeMorphism F (composeMorphism G H)).mapModel m := by
    rfl

/--
Associativity law for satisfaction preservation.

Both parenthesizations of a triple composite preserve satisfaction in the same
target system.
-/
theorem associativity_preserves_satisfaction
  {A B C D : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C)
  (H : PreservationMorphism C D)
  (m : A.Model)
  (φ : A.Sentence)
  (h : A.Sat m φ) :
  D.Sat
    ((composeMorphism (composeMorphism F G) H).mapModel m)
    ((composeMorphism (composeMorphism F G) H).translate φ) := by
      exact (composeMorphism (composeMorphism F G) H).preserves m φ h

end AlephOmega

namespace AlephOmega

/-
Concrete finite example.

This gives the abstract formal system an actual small finite model.

Models are Bool.
Sentences are Bool.
Satisfaction means equality.
-/

def BoolSystem : FormalSystem where
  Model := Bool
  Sentence := Bool
  Sat := fun m φ => m = φ

/--
A concrete satisfaction example.

The model true satisfies the sentence true.
-/
theorem bool_true_satisfies_true :
  BoolSystem.Sat true true := by
    rfl

/--
A concrete non-satisfaction example.

The model true does not satisfy the sentence false.
-/
theorem bool_true_not_satisfy_false :
  ¬ BoolSystem.Sat true false := by
    intro h
    cases h

/--
The identity morphism on the BoolSystem preserves satisfaction.
-/
theorem bool_identity_preserves :
  ∀ (m : BoolSystem.Model) (φ : BoolSystem.Sentence),
    BoolSystem.Sat m φ ->
    BoolSystem.Sat
      ((identityMorphism BoolSystem).mapModel m)
      ((identityMorphism BoolSystem).translate φ) := by
        intro m φ h
        exact identity_preserves_satisfaction BoolSystem m φ h

/--
The identity morphism composed with itself on BoolSystem preserves satisfaction.
-/
theorem bool_identity_composition_preserves :
  ∀ (m : BoolSystem.Model) (φ : BoolSystem.Sentence),
    BoolSystem.Sat m φ ->
    BoolSystem.Sat
      ((composeMorphism (identityMorphism BoolSystem) (identityMorphism BoolSystem)).mapModel m)
      ((composeMorphism (identityMorphism BoolSystem) (identityMorphism BoolSystem)).translate φ) := by
        intro m φ h
        exact
          composition_preserves_satisfaction
            (identityMorphism BoolSystem)
            (identityMorphism BoolSystem)
            m
            φ
            h

/--
A concrete check that the composed identity map sends true to true.
-/
theorem bool_identity_composition_true :
  ((composeMorphism (identityMorphism BoolSystem) (identityMorphism BoolSystem)).translate true) = true := by
    rfl

end AlephOmega

namespace AlephOmega

/-
Concrete failure boundary example.

The BoolSystem has:
- models = Bool
- sentences = Bool
- satisfaction = equality

Now define a bad translation that flips sentences but keeps models unchanged.

For m = true and φ = true:
- source satisfaction holds because true = true
- translated sentence is false
- target satisfaction fails because true ≠ false

This demonstrates a concrete failure of satisfaction preservation.
-/

/--
Sentence negation on Bool.
-/
def boolNegSentence : BoolSystem.Sentence -> BoolSystem.Sentence :=
  fun φ => not φ

/--
Model identity on Bool.
-/
def boolIdentityModel : BoolSystem.Model -> BoolSystem.Model :=
  fun m => m

/--
A concrete witness that the bad Bool translation fails preservation.
-/
theorem bool_bad_translation_failure :
  BoolSystem.Sat true true ∧
  ¬ BoolSystem.Sat (boolIdentityModel true) (boolNegSentence true) := by
    constructor
    · rfl
    · intro h
      cases h

/--
There cannot exist a proof that the bad Bool translation preserves satisfaction.
-/
theorem bool_bad_translation_not_preserving :
  ¬ (
    ∀ (m : BoolSystem.Model) (φ : BoolSystem.Sentence),
      BoolSystem.Sat m φ ->
      BoolSystem.Sat (boolIdentityModel m) (boolNegSentence φ)
  ) := by
    intro h
    have sourceSat : BoolSystem.Sat true true := by
      rfl
    have targetSat : BoolSystem.Sat (boolIdentityModel true) (boolNegSentence true) :=
      h true true sourceSat
    cases targetSat

/--
Failure boundary statement:

Satisfaction preservation is not automatic.
A sentence translation can destroy satisfaction.
-/
theorem preservation_not_automatic :
  ∃ (translate : BoolSystem.Sentence -> BoolSystem.Sentence)
    (mapModel : BoolSystem.Model -> BoolSystem.Model),
    ¬ (
      ∀ (m : BoolSystem.Model) (φ : BoolSystem.Sentence),
        BoolSystem.Sat m φ ->
        BoolSystem.Sat (mapModel m) (translate φ)
    ) := by
      exists boolNegSentence
      exists boolIdentityModel
      exact bool_bad_translation_not_preserving

end AlephOmega

namespace AlephOmega

/-
Phase 22A: Morphism equivalence.

Instead of claiming strict equality of preservation morphism structures, we define
an extensional equivalence relation.

Two preservation morphisms are equivalent when they have the same sentence
translation and the same model map.

This is mathematically cleaner because the proof fields may differ while the
actual morphism action is the same.
-/

/--
Extensional equivalence of satisfaction-preserving morphisms.
-/
def MorphismEquivalent
  {A B : FormalSystem}
  (F G : PreservationMorphism A B) : Prop :=
  (∀ φ : A.Sentence, F.translate φ = G.translate φ) ∧
  (∀ m : A.Model, F.mapModel m = G.mapModel m)

/--
Morphism equivalence is reflexive.
-/
theorem morphism_equiv_refl
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  MorphismEquivalent F F := by
    constructor
    · intro φ
      rfl
    · intro m
      rfl

/--
Morphism equivalence is symmetric.
-/
theorem morphism_equiv_symm
  {A B : FormalSystem}
  {F G : PreservationMorphism A B} :
  MorphismEquivalent F G -> MorphismEquivalent G F := by
    intro h
    constructor
    · intro φ
      exact Eq.symm (h.1 φ)
    · intro m
      exact Eq.symm (h.2 m)

/--
Morphism equivalence is transitive.
-/
theorem morphism_equiv_trans
  {A B : FormalSystem}
  {F G H : PreservationMorphism A B} :
  MorphismEquivalent F G ->
  MorphismEquivalent G H ->
  MorphismEquivalent F H := by
    intro hFG hGH
    constructor
    · intro φ
      exact Eq.trans (hFG.1 φ) (hGH.1 φ)
    · intro m
      exact Eq.trans (hFG.2 m) (hGH.2 m)

/--
Left identity law as morphism equivalence.
-/
theorem left_identity_equivalent
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  MorphismEquivalent (composeMorphism (identityMorphism A) F) F := by
    constructor
    · intro φ
      rfl
    · intro m
      rfl

/--
Right identity law as morphism equivalence.
-/
theorem right_identity_equivalent
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  MorphismEquivalent (composeMorphism F (identityMorphism B)) F := by
    constructor
    · intro φ
      rfl
    · intro m
      rfl

/--
Associativity law as morphism equivalence.
-/
theorem associativity_equivalent
  {A B C D : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C)
  (H : PreservationMorphism C D) :
  MorphismEquivalent
    (composeMorphism (composeMorphism F G) H)
    (composeMorphism F (composeMorphism G H)) := by
      constructor
      · intro φ
        rfl
      · intro m
        rfl

end AlephOmega

namespace AlephOmega

/-
Phase 22B: Composition respects morphism equivalence.

If two first-leg morphisms are equivalent and two second-leg morphisms are
equivalent, then their composites are equivalent.

This is a key compatibility condition for category-style reasoning up to
extensional equivalence.
-/

/--
Composition is compatible with morphism equivalence.
-/
theorem compose_respects_morphism_equivalence
  {A B C : FormalSystem}
  {F F' : PreservationMorphism A B}
  {G G' : PreservationMorphism B C} :
  MorphismEquivalent F F' ->
  MorphismEquivalent G G' ->
  MorphismEquivalent (composeMorphism F G) (composeMorphism F' G') := by
    intro hF hG
    constructor
    · intro φ
      calc
        G.translate (F.translate φ) = G.translate (F'.translate φ) := by
          rw [hF.1 φ]
        _ = G'.translate (F'.translate φ) := by
          exact hG.1 (F'.translate φ)
    · intro m
      calc
        G.mapModel (F.mapModel m) = G.mapModel (F'.mapModel m) := by
          rw [hF.2 m]
        _ = G'.mapModel (F'.mapModel m) := by
          exact hG.2 (F'.mapModel m)

/--
If two morphisms are equivalent, then satisfaction transported by one can be
viewed as satisfaction transported by the other.
-/
theorem equivalent_morphisms_transport_satisfaction
  {A B : FormalSystem}
  {F G : PreservationMorphism A B} :
  MorphismEquivalent F G ->
  ∀ (m : A.Model) (φ : A.Sentence),
    A.Sat m φ ->
    B.Sat (G.mapModel m) (G.translate φ) := by
      intro hEq m φ hSat
      rw [← hEq.2 m, ← hEq.1 φ]
      exact F.preserves m φ hSat

/--
Equivalent morphisms have equivalent composites after composition on the left.
-/
theorem left_composition_respects_equivalence
  {A B C : FormalSystem}
  {F F' : PreservationMorphism A B}
  (G : PreservationMorphism B C) :
  MorphismEquivalent F F' ->
  MorphismEquivalent (composeMorphism F G) (composeMorphism F' G) := by
    intro hF
    exact compose_respects_morphism_equivalence hF (morphism_equiv_refl G)

/--
Equivalent morphisms have equivalent composites after composition on the right.
-/
theorem right_composition_respects_equivalence
  {A B C : FormalSystem}
  (F : PreservationMorphism A B)
  {G G' : PreservationMorphism B C} :
  MorphismEquivalent G G' ->
  MorphismEquivalent (composeMorphism F G) (composeMorphism F G') := by
    intro hG
    exact compose_respects_morphism_equivalence (morphism_equiv_refl F) hG

end AlephOmega

namespace AlephOmega

/-
Phase 22D: Setoid and quotient hom-type prototype.

We now package morphism equivalence as a Setoid.

This is the first Lean-level step toward quotienting preservation morphisms by
extensional equivalence.
-/

/--
The Setoid of preservation morphisms under extensional equivalence.
-/
instance morphismSetoid
  {A B : FormalSystem} :
  Setoid (PreservationMorphism A B) where
    r := MorphismEquivalent
    iseqv := by
      constructor
      · intro F
        exact morphism_equiv_refl F
      · intro F G h
        exact morphism_equiv_symm h
      · intro F G H hFG hGH
        exact morphism_equiv_trans hFG hGH

/--
Quotient hom-type.

A quotient morphism from A to B is an equivalence class of
satisfaction-preserving morphisms from A to B.
-/
def QuotientMorphism
  (A B : FormalSystem) : Type :=
  Quotient (@morphismSetoid A B)

/--
The quotient identity arrow.
-/
def quotientIdentity
  (A : FormalSystem) : QuotientMorphism A A :=
  Quotient.mk morphismSetoid (identityMorphism A)

/--
Send a preservation morphism to its quotient class.
-/
def quotientOf
  {A B : FormalSystem}
  (F : PreservationMorphism A B) : QuotientMorphism A B :=
  Quotient.mk morphismSetoid F

/--
Equivalent morphisms determine the same quotient morphism.

This is the first quotient correctness theorem.
-/
theorem equivalent_morphisms_same_quotient
  {A B : FormalSystem}
  {F G : PreservationMorphism A B} :
  MorphismEquivalent F G ->
  quotientOf F = quotientOf G := by
    intro h
    exact Quotient.sound h

/--
Every morphism has the same quotient class as itself.
-/
theorem quotient_refl
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  quotientOf F = quotientOf F := by
    rfl

/--
Identity quotient is the quotient of the identity morphism.
-/
theorem quotient_identity_def
  (A : FormalSystem) :
  quotientIdentity A = quotientOf (identityMorphism A) := by
    rfl

end AlephOmega

namespace AlephOmega

/-
Phase 22E: Quotient composition well-definedness.

A quotient category needs composition to be independent of representative choice.

This theorem says:

If F is equivalent to F' and G is equivalent to G',
then the quotient class of G after F is the same as the quotient class of
G' after F'.

This is the core well-definedness theorem for quotient composition.
-/

/--
Quotient composition is well-defined with respect to morphism equivalence.
-/
theorem quotient_composition_well_defined
  {A B C : FormalSystem}
  {F F' : PreservationMorphism A B}
  {G G' : PreservationMorphism B C} :
  MorphismEquivalent F F' ->
  MorphismEquivalent G G' ->
  quotientOf (composeMorphism F G) = quotientOf (composeMorphism F' G') := by
    intro hF hG
    exact equivalent_morphisms_same_quotient
      (compose_respects_morphism_equivalence hF hG)

/--
Left representative change does not change the quotient composite.
-/
theorem quotient_left_representative_change
  {A B C : FormalSystem}
  {F F' : PreservationMorphism A B}
  (G : PreservationMorphism B C) :
  MorphismEquivalent F F' ->
  quotientOf (composeMorphism F G) = quotientOf (composeMorphism F' G) := by
    intro hF
    exact quotient_composition_well_defined hF (morphism_equiv_refl G)

/--
Right representative change does not change the quotient composite.
-/
theorem quotient_right_representative_change
  {A B C : FormalSystem}
  (F : PreservationMorphism A B)
  {G G' : PreservationMorphism B C} :
  MorphismEquivalent G G' ->
  quotientOf (composeMorphism F G) = quotientOf (composeMorphism F G') := by
    intro hG
    exact quotient_composition_well_defined (morphism_equiv_refl F) hG

/--
The quotient class of identity composed on the left is the quotient class of F.
-/
theorem quotient_left_identity
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  quotientOf (composeMorphism (identityMorphism A) F) = quotientOf F := by
    exact equivalent_morphisms_same_quotient (left_identity_equivalent F)

/--
The quotient class of identity composed on the right is the quotient class of F.
-/
theorem quotient_right_identity
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  quotientOf (composeMorphism F (identityMorphism B)) = quotientOf F := by
    exact equivalent_morphisms_same_quotient (right_identity_equivalent F)

/--
Associativity holds at the quotient-class level.
-/
theorem quotient_associativity
  {A B C D : FormalSystem}
  (F : PreservationMorphism A B)
  (G : PreservationMorphism B C)
  (H : PreservationMorphism C D) :
  quotientOf (composeMorphism (composeMorphism F G) H) =
  quotientOf (composeMorphism F (composeMorphism G H)) := by
    exact equivalent_morphisms_same_quotient (associativity_equivalent F G H)

end AlephOmega

namespace AlephOmega

/-
Phase 23A: Quotient composition as an actual operation.

Phase 22 proved quotient composition is well-defined.

Now we use that theorem to define composition directly on quotient morphisms.
-/

/--
Composition of quotient morphisms.

Given quotient arrows [F] : A -> B and [G] : B -> C, define their composite as
[G ∘ F] : A -> C.
-/
def quotientCompose
  {A B C : FormalSystem}
  (qF : QuotientMorphism A B)
  (qG : QuotientMorphism B C) :
  QuotientMorphism A C :=
  Quotient.liftOn₂ qF qG
    (fun F G => quotientOf (composeMorphism F G))
    (by
      intro F F' G G' hF hG
      exact quotient_composition_well_defined hF hG)

/--
Quotient left identity law.

The quotient identity composed on the left acts as identity.
-/
theorem quotient_category_left_identity
  {A B : FormalSystem}
  (qF : QuotientMorphism A B) :
  quotientCompose (quotientIdentity A) qF = qF := by
    refine Quotient.inductionOn qF ?_
    intro F
    exact quotient_left_identity F

/--
Quotient right identity law.

The quotient identity composed on the right acts as identity.
-/
theorem quotient_category_right_identity
  {A B : FormalSystem}
  (qF : QuotientMorphism A B) :
  quotientCompose qF (quotientIdentity B) = qF := by
    refine Quotient.inductionOn qF ?_
    intro F
    exact quotient_right_identity F

/--
Quotient associativity law.

Composition of quotient morphisms is associative.
-/
theorem quotient_category_associativity
  {A B C D : FormalSystem}
  (qF : QuotientMorphism A B)
  (qG : QuotientMorphism B C)
  (qH : QuotientMorphism C D) :
  quotientCompose (quotientCompose qF qG) qH =
  quotientCompose qF (quotientCompose qG qH) := by
    refine Quotient.inductionOn qF ?_
    intro F
    refine Quotient.inductionOn qG ?_
    intro G
    refine Quotient.inductionOn qH ?_
    intro H
    exact quotient_associativity F G H

end AlephOmega

namespace AlephOmega

/-
Phase 23B: Standalone quotient category API.

This section packages the quotient-category core into clean names.

The goal is not yet to instantiate Mathlib's Category typeclass.
The goal is to expose a standalone category-like API for quotient morphisms.
-/

/--
Quotient hom-type API name.

A quotient hom from A to B is a quotient morphism from A to B.
-/
abbrev QuotientHom
  (A B : FormalSystem) : Type :=
  QuotientMorphism A B

/--
Identity arrow in the standalone quotient category API.
-/
def quotientId
  (A : FormalSystem) : QuotientHom A A :=
  quotientIdentity A

/--
Composition in the standalone quotient category API.

The order is quotientComp F G = G after F.
-/
def quotientComp
  {A B C : FormalSystem}
  (F : QuotientHom A B)
  (G : QuotientHom B C) :
  QuotientHom A C :=
  quotientCompose F G

/--
Standalone quotient category left identity law.
-/
theorem quotient_api_left_identity
  {A B : FormalSystem}
  (F : QuotientHom A B) :
  quotientComp (quotientId A) F = F := by
    exact quotient_category_left_identity F

/--
Standalone quotient category right identity law.
-/
theorem quotient_api_right_identity
  {A B : FormalSystem}
  (F : QuotientHom A B) :
  quotientComp F (quotientId B) = F := by
    exact quotient_category_right_identity F

/--
Standalone quotient category associativity law.
-/
theorem quotient_api_associativity
  {A B C D : FormalSystem}
  (F : QuotientHom A B)
  (G : QuotientHom B C)
  (H : QuotientHom C D) :
  quotientComp (quotientComp F G) H =
  quotientComp F (quotientComp G H) := by
    exact quotient_category_associativity F G H

/--
Every preservation morphism determines a quotient hom.
-/
def quotientHomOf
  {A B : FormalSystem}
  (F : PreservationMorphism A B) :
  QuotientHom A B :=
  quotientOf F

/--
Equivalent preservation morphisms determine the same quotient hom.
-/
theorem quotient_hom_ext
  {A B : FormalSystem}
  {F G : PreservationMorphism A B} :
  MorphismEquivalent F G ->
  quotientHomOf F = quotientHomOf G := by
    intro h
    exact equivalent_morphisms_same_quotient h

/--
The quotient identity API agrees with the quotient of the identity morphism.
-/
theorem quotient_id_is_identity_class
  (A : FormalSystem) :
  quotientId A = quotientHomOf (identityMorphism A) := by
    rfl

end AlephOmega

namespace AlephOmega

/-
Phase 23C: Standalone quotient category structure.

This defines a small Aleph-Omega-specific category-like structure directly in Lean.

It is intentionally independent of Mathlib's Category typeclass.
-/

/--
A standalone quotient category structure for Project Aleph-Omega.

Objects are fixed to be FormalSystem values.

This avoids unnecessary universe-level complexity while still packaging:

- hom-types
- identity arrows
- composition
- left identity law
- right identity law
- associativity law
-/
structure StandaloneQuotientCategory where
  Hom : FormalSystem -> FormalSystem -> Type
  id : (A : FormalSystem) -> Hom A A
  comp : {A B C : FormalSystem} -> Hom A B -> Hom B C -> Hom A C
  left_id :
    ∀ {A B : FormalSystem} (F : Hom A B),
      comp (id A) F = F
  right_id :
    ∀ {A B : FormalSystem} (F : Hom A B),
      comp F (id B) = F
  assoc :
    ∀ {A B C D : FormalSystem}
      (F : Hom A B)
      (G : Hom B C)
      (H : Hom C D),
      comp (comp F G) H = comp F (comp G H)

/--
The Aleph-Omega standalone quotient category.

Arrows are quotient homs of satisfaction-preserving morphisms modulo
extensional equivalence.
-/
def AlephOmegaQuotientCategory : StandaloneQuotientCategory where
  Hom := QuotientHom
  id := quotientId
  comp := fun F G => quotientComp F G
  left_id := by
    intro A B F
    exact quotient_api_left_identity F
  right_id := by
    intro A B F
    exact quotient_api_right_identity F
  assoc := by
    intro A B C D F G H
    exact quotient_api_associativity F G H

/--
The hom-type of the Aleph-Omega quotient category is QuotientHom.
-/
theorem quotient_category_hom_is_quotient_hom
  (A B : FormalSystem) :
  AlephOmegaQuotientCategory.Hom A B = QuotientHom A B := by
    rfl

/--
The identity operation in the category structure agrees with quotientId.
-/
theorem quotient_category_id_is_quotient_id
  (A : FormalSystem) :
  AlephOmegaQuotientCategory.id A = quotientId A := by
    rfl

/--
The composition operation in the category structure agrees with quotientComp.
-/
theorem quotient_category_comp_is_quotient_comp
  {A B C : FormalSystem}
  (F : AlephOmegaQuotientCategory.Hom A B)
  (G : AlephOmegaQuotientCategory.Hom B C) :
  AlephOmegaQuotientCategory.comp F G = quotientComp F G := by
    rfl

end AlephOmega

namespace AlephOmega

/-
Phase 25A: Concrete two-model / two-sentence finite system.

This phase moves closer to the Python finite-universe layer by defining a
small finite formal system directly in Lean.

The system has:

- two models: m0 and m1
- two sentences: p and q
- satisfaction relation:
    m0 satisfies p
    m1 satisfies q
    no other satisfaction judgements hold
-/

inductive TwoModel where
  | m0
  | m1
deriving DecidableEq

inductive TwoSentence where
  | p
  | q
deriving DecidableEq

/--
A concrete finite system with two models and two sentences.
-/
def TwoSystem : FormalSystem where
  Model := TwoModel
  Sentence := TwoSentence
  Sat := fun m φ =>
    match m, φ with
    | TwoModel.m0, TwoSentence.p => True
    | TwoModel.m1, TwoSentence.q => True
    | _, _ => False

/--
m0 satisfies p.
-/
theorem two_m0_satisfies_p :
  TwoSystem.Sat TwoModel.m0 TwoSentence.p := by
    trivial

/--
m1 satisfies q.
-/
theorem two_m1_satisfies_q :
  TwoSystem.Sat TwoModel.m1 TwoSentence.q := by
    trivial

/--
m0 does not satisfy q.
-/
theorem two_m0_not_satisfy_q :
  ¬ TwoSystem.Sat TwoModel.m0 TwoSentence.q := by
    intro h
    cases h

/--
m1 does not satisfy p.
-/
theorem two_m1_not_satisfy_p :
  ¬ TwoSystem.Sat TwoModel.m1 TwoSentence.p := by
    intro h
    cases h

/--
The identity morphism on TwoSystem preserves satisfaction.
-/
theorem two_identity_preserves :
  ∀ (m : TwoSystem.Model) (φ : TwoSystem.Sentence),
    TwoSystem.Sat m φ ->
    TwoSystem.Sat
      ((identityMorphism TwoSystem).mapModel m)
      ((identityMorphism TwoSystem).translate φ) := by
        intro m φ h
        exact identity_preserves_satisfaction TwoSystem m φ h

/--
The identity morphism composed with itself on TwoSystem preserves satisfaction.
-/
theorem two_identity_composition_preserves :
  ∀ (m : TwoSystem.Model) (φ : TwoSystem.Sentence),
    TwoSystem.Sat m φ ->
    TwoSystem.Sat
      ((composeMorphism (identityMorphism TwoSystem) (identityMorphism TwoSystem)).mapModel m)
      ((composeMorphism (identityMorphism TwoSystem) (identityMorphism TwoSystem)).translate φ) := by
        intro m φ h
        exact
          composition_preserves_satisfaction
            (identityMorphism TwoSystem)
            (identityMorphism TwoSystem)
            m
            φ
            h

/--
A bad sentence translation that swaps p and q.
-/
def twoSwapSentence : TwoSystem.Sentence -> TwoSystem.Sentence :=
  fun φ =>
    match φ with
    | TwoSentence.p => TwoSentence.q
    | TwoSentence.q => TwoSentence.p

/--
A model map that keeps models fixed.
-/
def twoIdentityModel : TwoSystem.Model -> TwoSystem.Model :=
  fun m => m

/--
The swap translation does not preserve satisfaction.

m0 satisfies p, but m0 does not satisfy swap(p) = q.
-/
theorem two_swap_translation_failure :
  TwoSystem.Sat TwoModel.m0 TwoSentence.p ∧
  ¬ TwoSystem.Sat (twoIdentityModel TwoModel.m0) (twoSwapSentence TwoSentence.p) := by
    constructor
    · trivial
    · intro h
      cases h

/--
The swap translation is not satisfaction-preserving.
-/
theorem two_swap_translation_not_preserving :
  ¬ (
    ∀ (m : TwoSystem.Model) (φ : TwoSystem.Sentence),
      TwoSystem.Sat m φ ->
      TwoSystem.Sat (twoIdentityModel m) (twoSwapSentence φ)
  ) := by
    intro h
    have sourceSat : TwoSystem.Sat TwoModel.m0 TwoSentence.p := by
      trivial
    have targetSat :
      TwoSystem.Sat
        (twoIdentityModel TwoModel.m0)
        (twoSwapSentence TwoSentence.p) :=
      h TwoModel.m0 TwoSentence.p sourceSat
    cases targetSat

end AlephOmega

namespace AlephOmega

/-
Phase 25B: Nontrivial preservation morphism between two finite systems.

We define a second finite system with renamed models and renamed sentences.

Then we define a non-identity satisfaction-preserving morphism from TwoSystem
to RenamedTwoSystem.
-/

inductive RenamedModel where
  | a
  | b
deriving DecidableEq

inductive RenamedSentence where
  | alpha
  | beta
deriving DecidableEq

/--
A renamed finite system with two models and two sentences.

Satisfaction relation:

- a satisfies alpha
- b satisfies beta
- no other satisfaction judgements hold
-/
def RenamedTwoSystem : FormalSystem where
  Model := RenamedModel
  Sentence := RenamedSentence
  Sat := fun m φ =>
    match m, φ with
    | RenamedModel.a, RenamedSentence.alpha => True
    | RenamedModel.b, RenamedSentence.beta => True
    | _, _ => False

/--
Translation from TwoSystem sentences to RenamedTwoSystem sentences.
-/
def twoToRenamedSentence :
  TwoSystem.Sentence -> RenamedTwoSystem.Sentence :=
  fun φ =>
    match φ with
    | TwoSentence.p => RenamedSentence.alpha
    | TwoSentence.q => RenamedSentence.beta

/--
Model map from TwoSystem models to RenamedTwoSystem models.
-/
def twoToRenamedModel :
  TwoSystem.Model -> RenamedTwoSystem.Model :=
  fun m =>
    match m with
    | TwoModel.m0 => RenamedModel.a
    | TwoModel.m1 => RenamedModel.b

/--
The nontrivial map from TwoSystem to RenamedTwoSystem preserves satisfaction.
-/
theorem two_to_renamed_preserves :
  ∀ (m : TwoSystem.Model) (φ : TwoSystem.Sentence),
    TwoSystem.Sat m φ ->
    RenamedTwoSystem.Sat (twoToRenamedModel m) (twoToRenamedSentence φ) := by
      intro m φ h
      cases m <;> cases φ <;> simp [TwoSystem, RenamedTwoSystem, twoToRenamedModel, twoToRenamedSentence] at h ⊢

/--
A non-identity preservation morphism from TwoSystem to RenamedTwoSystem.
-/
def twoToRenamedMorphism :
  PreservationMorphism TwoSystem RenamedTwoSystem where
    translate := twoToRenamedSentence
    mapModel := twoToRenamedModel
    preserves := two_to_renamed_preserves

/--
Concrete preservation example: m0 satisfies p, and its image satisfies alpha.
-/
theorem two_to_renamed_m0_p :
  RenamedTwoSystem.Sat
    (twoToRenamedMorphism.mapModel TwoModel.m0)
    (twoToRenamedMorphism.translate TwoSentence.p) := by
      exact twoToRenamedMorphism.preserves TwoModel.m0 TwoSentence.p two_m0_satisfies_p

/--
Concrete preservation example: m1 satisfies q, and its image satisfies beta.
-/
theorem two_to_renamed_m1_q :
  RenamedTwoSystem.Sat
    (twoToRenamedMorphism.mapModel TwoModel.m1)
    (twoToRenamedMorphism.translate TwoSentence.q) := by
      exact twoToRenamedMorphism.preserves TwoModel.m1 TwoSentence.q two_m1_satisfies_q

/--
Composing the TwoSystem-to-RenamedTwoSystem morphism with identity preserves satisfaction.
-/
theorem two_to_renamed_then_identity_preserves :
  ∀ (m : TwoSystem.Model) (φ : TwoSystem.Sentence),
    TwoSystem.Sat m φ ->
    RenamedTwoSystem.Sat
      ((composeMorphism twoToRenamedMorphism (identityMorphism RenamedTwoSystem)).mapModel m)
      ((composeMorphism twoToRenamedMorphism (identityMorphism RenamedTwoSystem)).translate φ) := by
        intro m φ h
        exact
          composition_preserves_satisfaction
            twoToRenamedMorphism
            (identityMorphism RenamedTwoSystem)
            m
            φ
            h

/--
Composing identity with the TwoSystem-to-RenamedTwoSystem morphism preserves satisfaction.
-/
theorem identity_then_two_to_renamed_preserves :
  ∀ (m : TwoSystem.Model) (φ : TwoSystem.Sentence),
    TwoSystem.Sat m φ ->
    RenamedTwoSystem.Sat
      ((composeMorphism (identityMorphism TwoSystem) twoToRenamedMorphism).mapModel m)
      ((composeMorphism (identityMorphism TwoSystem) twoToRenamedMorphism).translate φ) := by
        intro m φ h
        exact
          composition_preserves_satisfaction
            (identityMorphism TwoSystem)
            twoToRenamedMorphism
            m
            φ
            h

end AlephOmega
