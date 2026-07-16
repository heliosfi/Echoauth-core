"""Direct evidence for the Stock Eligibility / Exclusion evaluator."""

from __future__ import annotations

import ast
import dataclasses
import inspect
import itertools
import json
import unittest
from pathlib import Path

import sniperbot.stock as stock_package
from sniperbot.stock import deferral_decision as deferral
from sniperbot.stock import eligibility_decision as subject
from sniperbot.stock.eligibility_decision import (
    AssetClass,
    AuthorityEvidence,
    Decision,
    GenericAssetClassContext,
    Outcome,
    ReasonCode,
    RequiredAction,
    StockEligibilityRequest,
    StockLaneConfirmation,
    Validity,
    create_request,
    evaluate,
)


REQUIRED_REQUEST_FIELDS = [
    "stock_reference",
    "eligibility_evidence_present",
    "eligibility_evidence_current",
    "eligibility_evidence_sufficient",
    "eligibility_evidence_contradictory",
    "stock_eligible",
    "stock_excluded",
    "stock_restricted",
    "eligibility_evidence_reference",
    "correlation_reference",
]


def required_values(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "stock_reference": " stock-ref ",
        "eligibility_evidence_present": True,
        "eligibility_evidence_current": True,
        "eligibility_evidence_sufficient": True,
        "eligibility_evidence_contradictory": False,
        "stock_eligible": True,
        "stock_excluded": False,
        "stock_restricted": False,
        "eligibility_evidence_reference": " evidence-ref ",
        "correlation_reference": " correlation-ref ",
    }
    values.update(changes)
    return values


def request(**changes: object) -> StockEligibilityRequest:
    values = required_values(stock_lane_confirmation=StockLaneConfirmation.CONFIRMED)
    values.update(changes)
    return create_request(**values)


def generic(**changes: object) -> GenericAssetClassContext:
    values: dict[str, object] = {
        "asset_class": AssetClass.STOCK,
        "validity": Validity.VALID,
        "current": True,
        "contradictory": False,
        "in_scope": True,
        "context_reference": " generic-ref ",
    }
    values.update(changes)
    return GenericAssetClassContext(**values)


def authority(**changes: object) -> AuthorityEvidence:
    values: dict[str, object] = {
        "validity": Validity.VALID,
        "current": True,
        "revoked": False,
        "contradictory": False,
        "in_scope": True,
        "evidence_reference": " authority-ref ",
    }
    values.update(changes)
    return AuthorityEvidence(**values)


def decision(**changes: object) -> Decision:
    values: dict[str, object] = {
        "outcome": Outcome.ELIGIBLE,
        "reason_code": ReasonCode.STOCK_ELIGIBLE,
        "required_action": RequiredAction.NONE,
        "stock_reference": "stock-ref",
        "eligibility_evidence_reference": "evidence-ref",
        "correlation_reference": "correlation-ref",
    }
    values.update(changes)
    return Decision(**values)


def oracle_generic_reason(context: GenericAssetClassContext) -> ReasonCode | None:
    if context.contradictory:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY
    if context.validity is Validity.AMBIGUOUS:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.validity is Validity.INVALID:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.asset_class is not AssetClass.STOCK:
        return ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK
    if not context.current:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE
    if not context.in_scope:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE
    return None


def oracle_authority_reason(evidence: AuthorityEvidence) -> ReasonCode | None:
    if evidence.contradictory:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity is Validity.AMBIGUOUS:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity is Validity.INVALID:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.revoked:
        return ReasonCode.AUTHORITY_EVIDENCE_REVOKED
    if not evidence.current:
        return ReasonCode.AUTHORITY_EVIDENCE_STALE
    if not evidence.in_scope:
        return ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE
    return None


def oracle(value: StockEligibilityRequest) -> tuple[Outcome, ReasonCode, RequiredAction]:
    if value.eligibility_evidence_contradictory:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY,
            RequiredAction.HUMAN_REVIEW,
        )
    if value.stock_eligible and value.stock_excluded:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBLE_EXCLUDED_CONFLICT,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if value.stock_eligible and value.stock_restricted:
        return (
            Outcome.RESTRICTED,
            ReasonCode.STOCK_ELIGIBLE_RESTRICTED_CONFLICT,
            RequiredAction.HUMAN_REVIEW,
        )
    undefined = (
        not value.eligibility_evidence_present and value.eligibility_evidence_current
    ) or (
        not value.eligibility_evidence_present and value.eligibility_evidence_sufficient
    ) or (
        not value.eligibility_evidence_current and value.eligibility_evidence_sufficient
    )
    if undefined:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.UNDEFINED_INPUT_COMBINATION,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if value.stock_lane_confirmation is None:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_LANE_CONFIRMATION_MISSING,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if value.stock_lane_confirmation is StockLaneConfirmation.CONTRADICTORY:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_LANE_CONTRADICTORY,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if value.stock_lane_confirmation is StockLaneConfirmation.NOT_CONFIRMED:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_LANE_NOT_CONFIRMED,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if value.generic_asset_class_context is not None:
        reason = oracle_generic_reason(value.generic_asset_class_context)
        if reason is not None:
            return Outcome.REVIEW_REQUIRED, reason, RequiredAction.GOVERNANCE_REVIEW
    if value.stock_excluded:
        return Outcome.EXCLUDED, ReasonCode.STOCK_EXCLUDED, RequiredAction.NONE
    if value.stock_restricted:
        return Outcome.RESTRICTED, ReasonCode.STOCK_RESTRICTED, RequiredAction.HUMAN_REVIEW
    if value.authority_evidence is not None:
        reason = oracle_authority_reason(value.authority_evidence)
        if reason is not None:
            return Outcome.REVIEW_REQUIRED, reason, RequiredAction.GOVERNANCE_REVIEW
    if not value.eligibility_evidence_present:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_MISSING,
            RequiredAction.HUMAN_REVIEW,
        )
    if not value.eligibility_evidence_current:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_STALE,
            RequiredAction.HUMAN_REVIEW,
        )
    if not value.eligibility_evidence_sufficient:
        return (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT,
            RequiredAction.HUMAN_REVIEW,
        )
    if value.stock_eligible:
        return Outcome.ELIGIBLE, ReasonCode.STOCK_ELIGIBLE, RequiredAction.NONE
    return (
        Outcome.REVIEW_REQUIRED,
        ReasonCode.STOCK_ELIGIBILITY_UNRESOLVED,
        RequiredAction.GOVERNANCE_REVIEW,
    )


class AlternateAuthority:
    validity = Validity.VALID
    current = True
    revoked = False
    contradictory = False
    in_scope = True
    evidence_reference = "alternate-authority"


class AlternateGenericContext:
    asset_class = AssetClass.STOCK
    validity = Validity.VALID
    current = True
    contradictory = False
    in_scope = True
    context_reference = "alternate-context"


class StockEligibilityExclusionTests(unittest.TestCase):
    def assert_mapping(
        self,
        value: StockEligibilityRequest,
        expected: tuple[Outcome, ReasonCode, RequiredAction],
    ) -> None:
        result = evaluate(value)
        self.assertEqual(
            (result.outcome, result.reason_code, result.required_action),
            expected,
        )

    def test_exact_public_api_and_enum_vocabularies(self) -> None:
        self.assertEqual(subject.__all__, [
            "AssetClass",
            "AuthorityEvidence",
            "Decision",
            "GenericAssetClassContext",
            "Outcome",
            "ReasonCode",
            "RequiredAction",
            "StockEligibilityRequest",
            "StockLaneConfirmation",
            "Validity",
            "create_request",
            "evaluate",
        ])
        expected = {
            AssetClass: ["STOCK", "OPTIONS", "CRYPTO"],
            StockLaneConfirmation: ["CONFIRMED", "NOT_CONFIRMED", "CONTRADICTORY"],
            Validity: ["VALID", "INVALID", "AMBIGUOUS"],
            Outcome: ["ELIGIBLE", "EXCLUDED", "RESTRICTED", "REVIEW_REQUIRED"],
            RequiredAction: [
                "NONE",
                "HUMAN_REVIEW",
                "GOVERNANCE_REVIEW",
                "FOUNDER_AUTHORITY_REQUIRED",
                "RESET_REQUIRED",
            ],
            ReasonCode: [
                "STOCK_ELIGIBLE",
                "STOCK_EXCLUDED",
                "STOCK_RESTRICTED",
                "STOCK_ELIGIBILITY_EVIDENCE_MISSING",
                "STOCK_ELIGIBILITY_EVIDENCE_STALE",
                "STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT",
                "STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY",
                "STOCK_ELIGIBLE_EXCLUDED_CONFLICT",
                "STOCK_ELIGIBLE_RESTRICTED_CONFLICT",
                "STOCK_LANE_CONFIRMATION_MISSING",
                "STOCK_LANE_NOT_CONFIRMED",
                "STOCK_LANE_CONTRADICTORY",
                "GENERIC_ASSET_CLASS_CONTEXT_INVALID",
                "GENERIC_ASSET_CLASS_CONTEXT_STALE",
                "GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY",
                "GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE",
                "GENERIC_ASSET_CLASS_NOT_STOCK",
                "AUTHORITY_EVIDENCE_INVALID",
                "AUTHORITY_EVIDENCE_STALE",
                "AUTHORITY_EVIDENCE_REVOKED",
                "AUTHORITY_EVIDENCE_OUT_OF_SCOPE",
                "UNDEFINED_INPUT_COMBINATION",
                "STOCK_ELIGIBILITY_UNRESOLVED",
            ],
        }
        for enum_type, values in expected.items():
            with self.subTest(enum=enum_type.__name__):
                self.assertEqual([member.value for member in enum_type], values)
                self.assertEqual(len(enum_type.__members__), len(list(enum_type)))
                self.assertTrue(issubclass(enum_type, str))
        self.assertFalse(hasattr(subject, "EmittableAction"))
        self.assertFalse(hasattr(subject, "EmittableReasonCode"))

    def test_exact_frozen_dataclass_contracts(self) -> None:
        expected = {
            GenericAssetClassContext: [
                ("asset_class", AssetClass),
                ("validity", Validity),
                ("current", bool),
                ("contradictory", bool),
                ("in_scope", bool),
                ("context_reference", str),
            ],
            AuthorityEvidence: [
                ("validity", Validity),
                ("current", bool),
                ("revoked", bool),
                ("contradictory", bool),
                ("in_scope", bool),
                ("evidence_reference", str),
            ],
            StockEligibilityRequest: [
                ("stock_reference", str),
                ("eligibility_evidence_present", bool),
                ("eligibility_evidence_current", bool),
                ("eligibility_evidence_sufficient", bool),
                ("eligibility_evidence_contradictory", bool),
                ("stock_eligible", bool),
                ("stock_excluded", bool),
                ("stock_restricted", bool),
                ("eligibility_evidence_reference", str),
                ("correlation_reference", str),
                ("stock_lane_confirmation", StockLaneConfirmation | None),
                ("generic_asset_class_context", GenericAssetClassContext | None),
                ("authority_evidence", AuthorityEvidence | None),
            ],
            Decision: [
                ("outcome", Outcome),
                ("reason_code", ReasonCode),
                ("required_action", RequiredAction),
                ("stock_reference", str),
                ("eligibility_evidence_reference", str),
                ("correlation_reference", str),
            ],
        }
        for dataclass_type, field_contract in expected.items():
            with self.subTest(dataclass=dataclass_type.__name__):
                annotations = inspect.get_annotations(dataclass_type, eval_str=True)
                actual_fields = dataclasses.fields(dataclass_type)
                self.assertEqual(
                    [(field.name, annotations[field.name]) for field in actual_fields],
                    field_contract,
                )
                self.assertTrue(dataclass_type.__dataclass_params__.frozen)
                self.assertTrue(all(field.default_factory is dataclasses.MISSING for field in actual_fields))
        request_fields = dataclasses.fields(StockEligibilityRequest)
        self.assertTrue(all(field.default is dataclasses.MISSING for field in request_fields[:10]))
        self.assertTrue(all(field.default is None for field in request_fields[10:]))
        for dataclass_type in (GenericAssetClassContext, AuthorityEvidence, Decision):
            self.assertTrue(all(field.default is dataclasses.MISSING for field in dataclasses.fields(dataclass_type)))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            request().stock_reference = "changed"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            generic().current = False
        with self.assertRaises(dataclasses.FrozenInstanceError):
            authority().revoked = True
        with self.assertRaises(dataclasses.FrozenInstanceError):
            decision().outcome = Outcome.EXCLUDED

    def test_exact_function_signatures(self) -> None:
        create_signature = inspect.signature(create_request)
        self.assertEqual(list(create_signature.parameters), ["values"])
        self.assertIs(
            create_signature.parameters["values"].kind,
            inspect.Parameter.VAR_KEYWORD,
        )
        create_annotations = inspect.get_annotations(create_request, eval_str=True)
        self.assertIs(create_annotations["values"], object)
        self.assertIs(create_annotations["return"], StockEligibilityRequest)
        evaluate_signature = inspect.signature(evaluate)
        self.assertEqual(list(evaluate_signature.parameters), ["request"])
        self.assertIs(
            evaluate_signature.parameters["request"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        evaluate_annotations = inspect.get_annotations(evaluate, eval_str=True)
        self.assertIs(evaluate_annotations["request"], StockEligibilityRequest)
        self.assertIs(evaluate_annotations["return"], Decision)

    def test_omission_and_explicit_none_boundaries(self) -> None:
        omitted = create_request(**required_values())
        self.assertIsNone(omitted.stock_lane_confirmation)
        self.assertIsNone(omitted.generic_asset_class_context)
        self.assertIsNone(omitted.authority_evidence)
        explicit_lane_none = create_request(**required_values(stock_lane_confirmation=None))
        self.assertIsNone(explicit_lane_none.stock_lane_confirmation)
        with self.assertRaises(TypeError):
            create_request(**required_values(generic_asset_class_context=None))
        with self.assertRaises(TypeError):
            create_request(**required_values(authority_evidence=None))
        direct = StockEligibilityRequest(
            **required_values(),
            stock_lane_confirmation=None,
            generic_asset_class_context=None,
            authority_evidence=None,
        )
        self.assertEqual(
            (direct.stock_lane_confirmation, direct.generic_asset_class_context, direct.authority_evidence),
            (None, None, None),
        )

    def test_missing_extra_positional_and_request_boolean_boundaries(self) -> None:
        for field in REQUIRED_REQUEST_FIELDS:
            values = required_values()
            del values[field]
            with self.subTest(missing=field), self.assertRaises(TypeError):
                create_request(**values)
        with self.assertRaises(TypeError):
            create_request(**required_values(unexpected=True))
        with self.assertRaises(TypeError):
            create_request(required_values())
        boolean_fields = [
            "eligibility_evidence_present",
            "eligibility_evidence_current",
            "eligibility_evidence_sufficient",
            "eligibility_evidence_contradictory",
            "stock_eligible",
            "stock_excluded",
            "stock_restricted",
        ]
        for field in boolean_fields:
            with self.subTest(boolean=field), self.assertRaises(TypeError):
                create_request(**required_values(**{field: 1}))

    def test_nested_fields_are_required_and_strict(self) -> None:
        for dataclass_type, values in (
            (
                GenericAssetClassContext,
                {
                    "asset_class": AssetClass.STOCK,
                    "validity": Validity.VALID,
                    "current": True,
                    "contradictory": False,
                    "in_scope": True,
                    "context_reference": "context",
                },
            ),
            (
                AuthorityEvidence,
                {
                    "validity": Validity.VALID,
                    "current": True,
                    "revoked": False,
                    "contradictory": False,
                    "in_scope": True,
                    "evidence_reference": "authority",
                },
            ),
        ):
            for field in values:
                missing = dict(values)
                del missing[field]
                with self.subTest(dataclass=dataclass_type.__name__, field=field), self.assertRaises(TypeError):
                    dataclass_type(**missing)
            for field in dataclasses.fields(dataclass_type):
                self.assertIs(field.default, dataclasses.MISSING)
                self.assertIs(field.default_factory, dataclasses.MISSING)
        for field in ("current", "contradictory", "in_scope"):
            with self.subTest(generic_boolean=field), self.assertRaises(TypeError):
                generic(**{field: 1})
        for field in ("current", "revoked", "contradictory", "in_scope"):
            with self.subTest(authority_boolean=field), self.assertRaises(TypeError):
                authority(**{field: 1})
        with self.assertRaises(TypeError):
            generic(asset_class="STOCK")
        with self.assertRaises(TypeError):
            generic(validity="VALID")
        with self.assertRaises(TypeError):
            authority(validity="VALID")
        with self.assertRaises(TypeError):
            request(stock_lane_confirmation="CONFIRMED")

    def test_alternate_subclass_and_deferral_shapes_are_rejected(self) -> None:
        class GenericSubclass(GenericAssetClassContext):
            pass

        class AuthoritySubclass(AuthorityEvidence):
            pass

        generic_subclass = GenericSubclass(
            AssetClass.STOCK,
            Validity.VALID,
            True,
            False,
            True,
            "generic-subclass",
        )
        authority_subclass = AuthoritySubclass(
            Validity.VALID,
            True,
            False,
            False,
            True,
            "authority-subclass",
        )
        invalid_generic_objects = (
            {},
            AlternateGenericContext(),
            generic_subclass,
            deferral.GenericAssetClassContext(
                deferral.AssetClass.STOCK,
                "VALID",
                True,
                False,
                True,
                "deferral-context",
            ),
        )
        invalid_authority_objects = (
            {},
            AlternateAuthority(),
            authority_subclass,
            deferral.AuthorityEvidence(
                "VALID",
                True,
                False,
                False,
                True,
                "deferral-authority",
            ),
        )
        for value in invalid_generic_objects:
            with self.subTest(generic=type(value).__name__), self.assertRaises(TypeError):
                request(generic_asset_class_context=value)
        for value in invalid_authority_objects:
            with self.subTest(authority=type(value).__name__), self.assertRaises(TypeError):
                request(authority_evidence=value)

    def test_reference_type_content_and_preservation_boundaries(self) -> None:
        for field in ("stock_reference", "eligibility_evidence_reference", "correlation_reference"):
            with self.subTest(request_type=field), self.assertRaises(TypeError):
                request(**{field: 7})
            for invalid in ("", " \t "):
                with self.subTest(request_content=field, invalid=invalid), self.assertRaises(ValueError):
                    request(**{field: invalid})
        with self.assertRaises(TypeError):
            generic(context_reference=7)
        with self.assertRaises(ValueError):
            generic(context_reference=" \t ")
        with self.assertRaises(TypeError):
            authority(evidence_reference=7)
        with self.assertRaises(ValueError):
            authority(evidence_reference=" \t ")
        for field in ("stock_reference", "eligibility_evidence_reference", "correlation_reference"):
            with self.subTest(decision_type=field), self.assertRaises(TypeError):
                decision(**{field: 7})
            with self.subTest(decision_content=field), self.assertRaises(ValueError):
                decision(**{field: " \t "})
        value = request(
            stock_reference="  stock  ",
            eligibility_evidence_reference="  evidence  ",
            correlation_reference="  correlation  ",
        )
        result = evaluate(value)
        self.assertEqual(result.stock_reference, "  stock  ")
        self.assertEqual(result.eligibility_evidence_reference, "  evidence  ")
        self.assertEqual(result.correlation_reference, "  correlation  ")

    def test_decision_enum_action_and_evaluate_type_boundaries(self) -> None:
        with self.assertRaises(TypeError):
            decision(outcome="ELIGIBLE")
        with self.assertRaises(TypeError):
            decision(reason_code="STOCK_ELIGIBLE")
        with self.assertRaises(TypeError):
            decision(required_action="NONE")
        for action in (RequiredAction.FOUNDER_AUTHORITY_REQUIRED, RequiredAction.RESET_REQUIRED):
            with self.subTest(action=action), self.assertRaises(ValueError):
                decision(required_action=action)
        for action in (
            RequiredAction.NONE,
            RequiredAction.HUMAN_REVIEW,
            RequiredAction.GOVERNANCE_REVIEW,
        ):
            self.assertIs(decision(required_action=action).required_action, action)
        for enum_type in (
            AssetClass,
            StockLaneConfirmation,
            Validity,
            Outcome,
            ReasonCode,
            RequiredAction,
        ):
            with self.subTest(enum=enum_type.__name__), self.assertRaises(ValueError):
                enum_type("UNKNOWN")
        for value in (object(), {}, deferral.create_request(
            stock_reference="stock",
            stock_evidence_present=True,
            stock_evidence_current=True,
            stock_evidence_sufficient=True,
            stock_evidence_contradictory=False,
            stock_deferral=False,
            stock_no_action=False,
            stock_restricted=False,
            stock_excluded=False,
            correlation_reference="correlation",
            stock_lane_confirmation=deferral.StockLaneConfirmation.CONFIRMED,
        )):
            with self.subTest(evaluate_type=type(value).__name__), self.assertRaises(TypeError):
                evaluate(value)

        class RequestSubclass(StockEligibilityRequest):
            pass

        subclass = RequestSubclass(
            **required_values(),
            stock_lane_confirmation=StockLaneConfirmation.CONFIRMED,
        )
        with self.assertRaises(TypeError):
            evaluate(subclass)

    def test_all_sixteen_branches_and_exact_mappings(self) -> None:
        cases = [
            (
                {"eligibility_evidence_contradictory": True},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW),
            ),
            (
                {"stock_excluded": True},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {"stock_restricted": True},
                (Outcome.RESTRICTED, ReasonCode.STOCK_ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW),
            ),
            (
                {"eligibility_evidence_present": False, "eligibility_evidence_sufficient": False},
                (Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {"stock_lane_confirmation": None},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_LANE_CONFIRMATION_MISSING, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {"stock_lane_confirmation": StockLaneConfirmation.CONTRADICTORY},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_LANE_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {"stock_lane_confirmation": StockLaneConfirmation.NOT_CONFIRMED},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_LANE_NOT_CONFIRMED, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {"generic_asset_class_context": generic(contradictory=True)},
                (Outcome.REVIEW_REQUIRED, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {"stock_eligible": False, "stock_excluded": True},
                (Outcome.EXCLUDED, ReasonCode.STOCK_EXCLUDED, RequiredAction.NONE),
            ),
            (
                {"stock_eligible": False, "stock_restricted": True},
                (Outcome.RESTRICTED, ReasonCode.STOCK_RESTRICTED, RequiredAction.HUMAN_REVIEW),
            ),
            (
                {"authority_evidence": authority(contradictory=True)},
                (Outcome.REVIEW_REQUIRED, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                {
                    "eligibility_evidence_present": False,
                    "eligibility_evidence_current": False,
                    "eligibility_evidence_sufficient": False,
                },
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW),
            ),
            (
                {"eligibility_evidence_current": False, "eligibility_evidence_sufficient": False},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW),
            ),
            (
                {"eligibility_evidence_sufficient": False},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW),
            ),
            (
                {},
                (Outcome.ELIGIBLE, ReasonCode.STOCK_ELIGIBLE, RequiredAction.NONE),
            ),
            (
                {"stock_eligible": False},
                (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW),
            ),
        ]
        self.assertEqual(len(cases), 16)
        for index, (changes, expected) in enumerate(cases, start=1):
            with self.subTest(branch=index):
                self.assert_mapping(request(**changes), expected)

    def test_all_postures_and_governed_undefined_predicates(self) -> None:
        posture_mappings = {
            (False, False, False): (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW),
            (False, False, True): (Outcome.RESTRICTED, ReasonCode.STOCK_RESTRICTED, RequiredAction.HUMAN_REVIEW),
            (False, True, False): (Outcome.EXCLUDED, ReasonCode.STOCK_EXCLUDED, RequiredAction.NONE),
            (False, True, True): (Outcome.EXCLUDED, ReasonCode.STOCK_EXCLUDED, RequiredAction.NONE),
            (True, False, False): (Outcome.ELIGIBLE, ReasonCode.STOCK_ELIGIBLE, RequiredAction.NONE),
            (True, False, True): (Outcome.RESTRICTED, ReasonCode.STOCK_ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW),
            (True, True, False): (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            (True, True, True): (Outcome.REVIEW_REQUIRED, ReasonCode.STOCK_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
        }
        for posture, expected in posture_mappings.items():
            with self.subTest(posture=posture):
                self.assert_mapping(request(
                    stock_eligible=posture[0],
                    stock_excluded=posture[1],
                    stock_restricted=posture[2],
                ), expected)
        undefined_states = (
            (False, True, False),
            (False, False, True),
            (True, False, True),
        )
        for present, current, sufficient in undefined_states:
            with self.subTest(undefined=(present, current, sufficient)):
                self.assert_mapping(request(
                    eligibility_evidence_present=present,
                    eligibility_evidence_current=current,
                    eligibility_evidence_sufficient=sufficient,
                ), (
                    Outcome.REVIEW_REQUIRED,
                    ReasonCode.UNDEFINED_INPUT_COMBINATION,
                    RequiredAction.GOVERNANCE_REVIEW,
                ))

    def test_generic_states_and_all_fourteen_pairwise_collisions(self) -> None:
        states = ["contradictory", "ambiguous", "invalid", "non_stock", "stale", "out_of_scope"]
        reason_by_state = {
            "contradictory": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY,
            "ambiguous": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID,
            "invalid": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID,
            "non_stock": ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK,
            "stale": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE,
            "out_of_scope": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE,
        }

        def build(active: set[str]) -> GenericAssetClassContext:
            validity = Validity.VALID
            if "ambiguous" in active:
                validity = Validity.AMBIGUOUS
            if "invalid" in active:
                validity = Validity.INVALID
            return generic(
                asset_class=AssetClass.OPTIONS if "non_stock" in active else AssetClass.STOCK,
                validity=validity,
                current="stale" not in active,
                contradictory="contradictory" in active,
                in_scope="out_of_scope" not in active,
            )

        for state in states:
            self.assert_mapping(request(generic_asset_class_context=build({state})), (
                Outcome.REVIEW_REQUIRED,
                reason_by_state[state],
                RequiredAction.GOVERNANCE_REVIEW,
            ))
        collisions = [
            pair for pair in itertools.combinations(states, 2)
            if set(pair) != {"ambiguous", "invalid"}
        ]
        self.assertEqual(len(collisions), 14)
        for pair in collisions:
            winner = min(pair, key=states.index)
            with self.subTest(collision=pair):
                self.assert_mapping(request(generic_asset_class_context=build(set(pair))), (
                    Outcome.REVIEW_REQUIRED,
                    reason_by_state[winner],
                    RequiredAction.GOVERNANCE_REVIEW,
                ))
        self.assert_mapping(request(generic_asset_class_context=generic(in_scope=False)), (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE,
            RequiredAction.GOVERNANCE_REVIEW,
        ))

    def test_authority_states_and_all_fourteen_pairwise_collisions(self) -> None:
        states = ["contradictory", "ambiguous", "invalid", "revoked", "stale", "out_of_scope"]
        reason_by_state = {
            "contradictory": ReasonCode.AUTHORITY_EVIDENCE_INVALID,
            "ambiguous": ReasonCode.AUTHORITY_EVIDENCE_INVALID,
            "invalid": ReasonCode.AUTHORITY_EVIDENCE_INVALID,
            "revoked": ReasonCode.AUTHORITY_EVIDENCE_REVOKED,
            "stale": ReasonCode.AUTHORITY_EVIDENCE_STALE,
            "out_of_scope": ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE,
        }

        def build(active: set[str]) -> AuthorityEvidence:
            validity = Validity.VALID
            if "ambiguous" in active:
                validity = Validity.AMBIGUOUS
            if "invalid" in active:
                validity = Validity.INVALID
            return authority(
                validity=validity,
                current="stale" not in active,
                revoked="revoked" in active,
                contradictory="contradictory" in active,
                in_scope="out_of_scope" not in active,
            )

        for state in states:
            self.assert_mapping(request(authority_evidence=build({state})), (
                Outcome.REVIEW_REQUIRED,
                reason_by_state[state],
                RequiredAction.GOVERNANCE_REVIEW,
            ))
        collisions = [
            pair for pair in itertools.combinations(states, 2)
            if set(pair) != {"ambiguous", "invalid"}
        ]
        self.assertEqual(len(collisions), 14)
        for pair in collisions:
            winner = min(pair, key=states.index)
            with self.subTest(collision=pair):
                self.assert_mapping(request(authority_evidence=build(set(pair))), (
                    Outcome.REVIEW_REQUIRED,
                    reason_by_state[winner],
                    RequiredAction.GOVERNANCE_REVIEW,
                ))
        self.assert_mapping(request(authority_evidence=authority(in_scope=False)), (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE,
            RequiredAction.GOVERNANCE_REVIEW,
        ))

    def test_absent_and_valid_contexts_continue_without_granting_eligibility(self) -> None:
        unresolved = (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_UNRESOLVED,
            RequiredAction.GOVERNANCE_REVIEW,
        )
        self.assert_mapping(request(stock_eligible=False), unresolved)
        self.assert_mapping(request(stock_eligible=False, generic_asset_class_context=generic()), unresolved)
        self.assert_mapping(request(stock_eligible=False, authority_evidence=authority()), unresolved)
        self.assert_mapping(request(
            stock_eligible=False,
            generic_asset_class_context=generic(),
            authority_evidence=authority(),
        ), unresolved)

    def test_reference_preservation_purity_nonmutation_and_repetition(self) -> None:
        context = generic(context_reference="  generic exact  ")
        evidence = authority(evidence_reference="  authority exact  ")
        value = request(
            stock_reference="  stock exact  ",
            eligibility_evidence_reference="  eligibility exact  ",
            correlation_reference="  correlation exact  ",
            generic_asset_class_context=context,
            authority_evidence=evidence,
        )
        request_before = dataclasses.asdict(value)
        context_before = dataclasses.asdict(context)
        authority_before = dataclasses.asdict(evidence)
        first = evaluate(value)
        second = evaluate(value)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertIsNot(first, value)
        self.assertIsNot(first, context)
        self.assertIsNot(first, evidence)
        self.assertEqual(dataclasses.asdict(value), request_before)
        self.assertEqual(dataclasses.asdict(context), context_before)
        self.assertEqual(dataclasses.asdict(evidence), authority_before)
        self.assertEqual(first.stock_reference, value.stock_reference)
        self.assertEqual(first.eligibility_evidence_reference, value.eligibility_evidence_reference)
        self.assertEqual(first.correlation_reference, value.correlation_reference)
        self.assertEqual(context.context_reference, "  generic exact  ")
        self.assertEqual(evidence.evidence_reference, "  authority exact  ")

    def test_schema_api_parity(self) -> None:
        schema = json.loads(Path(
            "schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json"
        ).read_text(encoding="utf-8"))
        definitions = schema["$defs"]
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(
            schema["$id"],
            "https://echoauth.local/schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json",
        )
        self.assertEqual(schema["required"], ["request", "decision"])
        self.assertEqual(list(schema["properties"]), ["request", "decision"])
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(list(definitions), [
            "AssetClass",
            "StockLaneConfirmation",
            "Validity",
            "Outcome",
            "ReasonCode",
            "RequiredAction",
            "EmittableAction",
            "GenericAssetClassContext",
            "AuthorityEvidence",
            "Request",
            "Decision",
        ])
        enum_definitions = {
            AssetClass: "AssetClass",
            StockLaneConfirmation: "StockLaneConfirmation",
            Validity: "Validity",
            Outcome: "Outcome",
            ReasonCode: "ReasonCode",
            RequiredAction: "RequiredAction",
        }
        for enum_type, definition in enum_definitions.items():
            self.assertEqual(
                [member.value for member in enum_type],
                definitions[definition]["enum"],
            )
        dataclass_definitions = {
            GenericAssetClassContext: "GenericAssetClassContext",
            AuthorityEvidence: "AuthorityEvidence",
            StockEligibilityRequest: "Request",
            Decision: "Decision",
        }
        for dataclass_type, definition in dataclass_definitions.items():
            field_names = [field.name for field in dataclasses.fields(dataclass_type)]
            self.assertEqual(
                field_names,
                list(definitions[definition]["properties"]),
            )
            self.assertFalse(definitions[definition]["additionalProperties"])
            if definition != "Request":
                self.assertEqual(definitions[definition]["required"], field_names)
        self.assertEqual(definitions["Request"]["required"], REQUIRED_REQUEST_FIELDS)
        self.assertEqual(
            definitions["Request"]["properties"]["stock_lane_confirmation"]["oneOf"],
            [{"$ref": "#/$defs/StockLaneConfirmation"}, {"type": "null"}],
        )
        self.assertEqual(
            definitions["Request"]["properties"]["generic_asset_class_context"]["$ref"],
            "#/$defs/GenericAssetClassContext",
        )
        self.assertEqual(
            definitions["Request"]["properties"]["authority_evidence"]["$ref"],
            "#/$defs/AuthorityEvidence",
        )
        self.assertEqual(
            definitions["EmittableAction"]["enum"],
            [member.value for member in (
                RequiredAction.NONE,
                RequiredAction.HUMAN_REVIEW,
                RequiredAction.GOVERNANCE_REVIEW,
            )],
        )
        self.assertEqual(
            definitions["Decision"]["properties"]["required_action"],
            {"$ref": "#/$defs/EmittableAction"},
        )
        for definition, names in (
            ("Request", [
                "eligibility_evidence_present",
                "eligibility_evidence_current",
                "eligibility_evidence_sufficient",
                "eligibility_evidence_contradictory",
                "stock_eligible",
                "stock_excluded",
                "stock_restricted",
            ]),
            ("GenericAssetClassContext", ["current", "contradictory", "in_scope"]),
            ("AuthorityEvidence", ["current", "revoked", "contradictory", "in_scope"]),
        ):
            for name in names:
                self.assertEqual(
                    definitions[definition]["properties"][name]["type"],
                    "boolean",
                )
        for definition, names in (
            ("Request", [
                "stock_reference",
                "eligibility_evidence_reference",
                "correlation_reference",
            ]),
            ("GenericAssetClassContext", ["context_reference"]),
            ("AuthorityEvidence", ["evidence_reference"]),
            ("Decision", [
                "stock_reference",
                "eligibility_evidence_reference",
                "correlation_reference",
            ]),
        ):
            for name in names:
                reference_schema = definitions[definition]["properties"][name]
                self.assertEqual(reference_schema["type"], "string")
                self.assertEqual(reference_schema["minLength"], 1)
                self.assertEqual(reference_schema["pattern"], "\\S")

    def test_package_root_remains_stock_deferral_only(self) -> None:
        expected = [
            "AssetClass",
            "AuthorityEvidence",
            "Decision",
            "EmittableReasonCode",
            "GenericAssetClassContext",
            "Outcome",
            "ReasonCode",
            "RequiredAction",
            "StockLaneConfirmation",
            "StockRequest",
            "create_request",
            "evaluate",
        ]
        self.assertEqual(stock_package.__all__, expected)
        self.assertIs(stock_package.AssetClass, deferral.AssetClass)
        self.assertIs(stock_package.Decision, deferral.Decision)
        self.assertIs(stock_package.create_request, deferral.create_request)
        self.assertIsNot(stock_package.AssetClass, AssetClass)
        self.assertNotIn("StockEligibilityRequest", stock_package.__all__)
        self.assertNotIn("Validity", stock_package.__all__)
        initializer = Path("src/sniperbot/stock/__init__.py").read_text(encoding="utf-8")
        self.assertNotIn("eligibility_decision", initializer)
        self.assertNotIn("StockEligibilityRequest", initializer)

    def test_production_import_and_prohibited_capability_boundary(self) -> None:
        source = Path("src/sniperbot/stock/eligibility_decision.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.append((None, tuple(alias.name for alias in node.names)))
            elif isinstance(node, ast.ImportFrom):
                imports.append((node.module, tuple(alias.name for alias in node.names)))
        self.assertEqual(imports, [
            ("__future__", ("annotations",)),
            ("dataclasses", ("dataclass",)),
            ("enum", ("Enum",)),
        ])
        banned_calls = {
            "open",
            "exec",
            "eval",
            "compile",
            "__import__",
            "input",
            "breakpoint",
        }
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertFalse(called_names & banned_calls)
        prohibited_names = {
            "os",
            "sys",
            "socket",
            "subprocess",
            "requests",
            "urllib",
            "http",
            "pathlib",
            "time",
            "datetime",
            "random",
            "secrets",
            "logging",
            "sqlite3",
            "asyncio",
            "threading",
            "multiprocessing",
            "pickle",
            "shelve",
        }
        used_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        self.assertFalse(used_names & prohibited_names)
        self.assertFalse(any(isinstance(node, (ast.AsyncFunctionDef, ast.Await)) for node in ast.walk(tree)))
        self.assertFalse(any(
            isinstance(node, (ast.Global, ast.Nonlocal, ast.Delete, ast.Yield, ast.YieldFrom))
            for node in ast.walk(tree)
        ))

    def test_exhaustive_32768_combination_independent_oracle(self) -> None:
        generic_states = (
            None,
            generic(),
            generic(contradictory=True),
            generic(validity=Validity.AMBIGUOUS),
            generic(validity=Validity.INVALID),
            generic(asset_class=AssetClass.OPTIONS),
            generic(current=False),
            generic(in_scope=False),
        )
        authority_states = (
            None,
            authority(),
            authority(contradictory=True),
            authority(validity=Validity.AMBIGUOUS),
            authority(validity=Validity.INVALID),
            authority(revoked=True),
            authority(current=False),
            authority(in_scope=False),
        )
        lane_states = (
            None,
            StockLaneConfirmation.CONFIRMED,
            StockLaneConfirmation.NOT_CONFIRMED,
            StockLaneConfirmation.CONTRADICTORY,
        )
        count = 0
        seen_reasons: set[ReasonCode] = set()
        seen_actions: set[RequiredAction] = set()
        for evidence_facts in itertools.product((False, True), repeat=4):
            for posture in itertools.product((False, True), repeat=3):
                for lane in lane_states:
                    for context in generic_states:
                        for evidence in authority_states:
                            values = required_values(
                                eligibility_evidence_present=evidence_facts[0],
                                eligibility_evidence_current=evidence_facts[1],
                                eligibility_evidence_sufficient=evidence_facts[2],
                                eligibility_evidence_contradictory=evidence_facts[3],
                                stock_eligible=posture[0],
                                stock_excluded=posture[1],
                                stock_restricted=posture[2],
                                stock_lane_confirmation=lane,
                            )
                            if context is not None:
                                values["generic_asset_class_context"] = context
                            if evidence is not None:
                                values["authority_evidence"] = evidence
                            value = create_request(**values)
                            expected = oracle(value)
                            actual = evaluate(value)
                            self.assertEqual(
                                (actual.outcome, actual.reason_code, actual.required_action),
                                expected,
                            )
                            self.assertEqual(actual.stock_reference, value.stock_reference)
                            self.assertEqual(
                                actual.eligibility_evidence_reference,
                                value.eligibility_evidence_reference,
                            )
                            self.assertEqual(actual.correlation_reference, value.correlation_reference)
                            seen_reasons.add(actual.reason_code)
                            seen_actions.add(actual.required_action)
                            count += 1
        self.assertEqual(count, 32_768)
        self.assertEqual(seen_reasons, set(ReasonCode))
        self.assertEqual(seen_actions, {
            RequiredAction.NONE,
            RequiredAction.HUMAN_REVIEW,
            RequiredAction.GOVERNANCE_REVIEW,
        })


if __name__ == "__main__":
    unittest.main()
