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
