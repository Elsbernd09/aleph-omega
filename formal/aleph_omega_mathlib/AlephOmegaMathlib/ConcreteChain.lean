import AlephOmegaMathlib.QuotientFormalSystemCategory

namespace AlephOmegaMathlib

open CategoryTheory

/-
Phase 30E: Concrete three-system chain ported to the Mathlib track.

This ports the original standalone concrete chain into the experimental Mathlib
formalization.

The chain is:

  MathlibTwoSystem -> MathlibRenamedSystem -> MathlibThirdSystem

Each arrow is a satisfaction-preserving morphism.

The quotient classes of these morphisms also compose inside the experimental
Mathlib quotient category.
-/

inductive MathlibTwoModel where
  | m0
  | m1
deriving DecidableEq

inductive MathlibTwoSentence where
  | p
  | q
deriving DecidableEq

def MathlibTwoSystem : FormalSystem where
  Model := MathlibTwoModel
  Sentence := MathlibTwoSentence
  Sat := fun m φ =>
    match m, φ with
    | MathlibTwoModel.m0, MathlibTwoSentence.p => True
    | MathlibTwoModel.m1, MathlibTwoSentence.q => True
    | _, _ => False

inductive MathlibRenamedModel where
  | a
  | b
deriving DecidableEq

inductive MathlibRenamedSentence where
  | alpha
  | beta
deriving DecidableEq

def MathlibRenamedSystem : FormalSystem where
  Model := MathlibRenamedModel
  Sentence := MathlibRenamedSentence
  Sat := fun m φ =>
    match m, φ with
    | MathlibRenamedModel.a, MathlibRenamedSentence.alpha => True
    | MathlibRenamedModel.b, MathlibRenamedSentence.beta => True
    | _, _ => False

inductive MathlibThirdModel where
  | x
  | y
deriving DecidableEq

inductive MathlibThirdSentence where
  | gamma
  | delta
deriving DecidableEq

def MathlibThirdSystem : FormalSystem where
  Model := MathlibThirdModel
  Sentence := MathlibThirdSentence
  Sat := fun m φ =>
    match m, φ with
    | MathlibThirdModel.x, MathlibThirdSentence.gamma => True
    | MathlibThirdModel.y, MathlibThirdSentence.delta => True
    | _, _ => False

theorem mathlib_two_m0_satisfies_p :
  MathlibTwoSystem.Sat MathlibTwoModel.m0 MathlibTwoSentence.p := by
    trivial

theorem mathlib_two_m1_satisfies_q :
  MathlibTwoSystem.Sat MathlibTwoModel.m1 MathlibTwoSentence.q := by
    trivial

def mathlibTwoToRenamedSentence :
  MathlibTwoSystem.Sentence -> MathlibRenamedSystem.Sentence :=
  fun φ =>
    match φ with
    | MathlibTwoSentence.p => MathlibRenamedSentence.alpha
    | MathlibTwoSentence.q => MathlibRenamedSentence.beta

def mathlibTwoToRenamedModel :
  MathlibTwoSystem.Model -> MathlibRenamedSystem.Model :=
  fun m =>
    match m with
    | MathlibTwoModel.m0 => MathlibRenamedModel.a
    | MathlibTwoModel.m1 => MathlibRenamedModel.b

theorem mathlib_two_to_renamed_preserves :
  ∀ (m : MathlibTwoSystem.Model) (φ : MathlibTwoSystem.Sentence),
    MathlibTwoSystem.Sat m φ ->
    MathlibRenamedSystem.Sat
      (mathlibTwoToRenamedModel m)
      (mathlibTwoToRenamedSentence φ) := by
        intro m φ h
        cases m <;> cases φ <;>
          simp [
            MathlibTwoSystem,
            MathlibRenamedSystem,
            mathlibTwoToRenamedModel,
            mathlibTwoToRenamedSentence
          ] at h ⊢

def mathlibTwoToRenamedMorphism :
  PreservationMorphism MathlibTwoSystem MathlibRenamedSystem where
    translate := mathlibTwoToRenamedSentence
    mapModel := mathlibTwoToRenamedModel
    preserves := mathlib_two_to_renamed_preserves

def mathlibRenamedToThirdSentence :
  MathlibRenamedSystem.Sentence -> MathlibThirdSystem.Sentence :=
  fun φ =>
    match φ with
    | MathlibRenamedSentence.alpha => MathlibThirdSentence.gamma
    | MathlibRenamedSentence.beta => MathlibThirdSentence.delta

def mathlibRenamedToThirdModel :
  MathlibRenamedSystem.Model -> MathlibThirdSystem.Model :=
  fun m =>
    match m with
    | MathlibRenamedModel.a => MathlibThirdModel.x
    | MathlibRenamedModel.b => MathlibThirdModel.y

theorem mathlib_renamed_to_third_preserves :
  ∀ (m : MathlibRenamedSystem.Model) (φ : MathlibRenamedSystem.Sentence),
    MathlibRenamedSystem.Sat m φ ->
    MathlibThirdSystem.Sat
      (mathlibRenamedToThirdModel m)
      (mathlibRenamedToThirdSentence φ) := by
        intro m φ h
        cases m <;> cases φ <;>
          simp [
            MathlibRenamedSystem,
            MathlibThirdSystem,
            mathlibRenamedToThirdModel,
            mathlibRenamedToThirdSentence
          ] at h ⊢

def mathlibRenamedToThirdMorphism :
  PreservationMorphism MathlibRenamedSystem MathlibThirdSystem where
    translate := mathlibRenamedToThirdSentence
    mapModel := mathlibRenamedToThirdModel
    preserves := mathlib_renamed_to_third_preserves

def mathlibTwoToThirdComposite :
  PreservationMorphism MathlibTwoSystem MathlibThirdSystem :=
  composePreservation mathlibTwoToRenamedMorphism mathlibRenamedToThirdMorphism

theorem mathlib_two_to_third_composite_preserves :
  ∀ (m : MathlibTwoSystem.Model) (φ : MathlibTwoSystem.Sentence),
    MathlibTwoSystem.Sat m φ ->
    MathlibThirdSystem.Sat
      (mathlibTwoToThirdComposite.mapModel m)
      (mathlibTwoToThirdComposite.translate φ) := by
        intro m φ h
        exact mathlibTwoToThirdComposite.preserves m φ h

theorem mathlib_two_to_third_m0_p :
  MathlibThirdSystem.Sat
    (mathlibTwoToThirdComposite.mapModel MathlibTwoModel.m0)
    (mathlibTwoToThirdComposite.translate MathlibTwoSentence.p) := by
      exact
        mathlib_two_to_third_composite_preserves
          MathlibTwoModel.m0
          MathlibTwoSentence.p
          mathlib_two_m0_satisfies_p

theorem mathlib_two_to_third_m1_q :
  MathlibThirdSystem.Sat
    (mathlibTwoToThirdComposite.mapModel MathlibTwoModel.m1)
    (mathlibTwoToThirdComposite.translate MathlibTwoSentence.q) := by
      exact
        mathlib_two_to_third_composite_preserves
          MathlibTwoModel.m1
          MathlibTwoSentence.q
          mathlib_two_m1_satisfies_q

def qMathlibTwoToRenamed :
  QuotientPreservationHom MathlibTwoSystem MathlibRenamedSystem :=
  quotientPreservationOf mathlibTwoToRenamedMorphism

def qMathlibRenamedToThird :
  QuotientPreservationHom MathlibRenamedSystem MathlibThirdSystem :=
  quotientPreservationOf mathlibRenamedToThirdMorphism

def qMathlibTwoToThird :
  QuotientPreservationHom MathlibTwoSystem MathlibThirdSystem :=
  quotientPreservationOf mathlibTwoToThirdComposite

theorem q_mathlib_concrete_chain_composes :
  quotientComposePreservation qMathlibTwoToRenamed qMathlibRenamedToThird =
  qMathlibTwoToThird := by
    rfl

def QMathlibTwoSystem : QuotientFormalSystem where
  system := MathlibTwoSystem

def QMathlibRenamedSystem : QuotientFormalSystem where
  system := MathlibRenamedSystem

def QMathlibThirdSystem : QuotientFormalSystem where
  system := MathlibThirdSystem

def qCategoryMathlibTwoToRenamed :
  QMathlibTwoSystem ⟶ QMathlibRenamedSystem :=
  qMathlibTwoToRenamed

def qCategoryMathlibRenamedToThird :
  QMathlibRenamedSystem ⟶ QMathlibThirdSystem :=
  qMathlibRenamedToThird

def qCategoryMathlibTwoToThird :
  QMathlibTwoSystem ⟶ QMathlibThirdSystem :=
  qMathlibTwoToThird

theorem q_category_mathlib_concrete_chain_composes :
  qCategoryMathlibTwoToRenamed ≫ qCategoryMathlibRenamedToThird =
  qCategoryMathlibTwoToThird := by
    rfl

end AlephOmegaMathlib
