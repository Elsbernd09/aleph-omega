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
