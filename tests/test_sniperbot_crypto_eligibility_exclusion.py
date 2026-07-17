"""Direct evidence for the Crypto Eligibility / Exclusion evaluator."""

from __future__ import annotations

import ast
import dataclasses
import inspect
import itertools
import json
import re
import unittest
from pathlib import Path

import sniperbot.crypto as crypto_package
from sniperbot.crypto import deferral_decision as deferral
from sniperbot.crypto import eligibility_decision as subject
from sniperbot.eligibility import asset_class_decision as asset_class_eligibility
from sniperbot.options import eligibility_decision as options_eligibility
from sniperbot.stock import eligibility_decision as stock_eligibility
from sniperbot.crypto.eligibility_decision import (
    AssetClass,
    AuthorityEvidence,
    CryptoEligibilityRequest,
    CryptoLaneConfirmation,
    Decision,
    GenericAssetClassContext,
    Outcome,
    ReasonCode,
    RequiredAction,
    Validity,
    create_request,
    evaluate,
)


REQUIRED_REQUEST_FIELDS = [
    "crypto_reference",
    "eligibility_evidence_present",
    "eligibility_evidence_current",
    "eligibility_evidence_sufficient",
    "eligibility_evidence_contradictory",
    "crypto_eligible",
    "crypto_excluded",
    "crypto_restricted",
    "eligibility_evidence_reference",
    "correlation_reference",
]


def required_values(**changes: object) -> dict[str, object]:
    values: dict[str, object] = {
        "crypto_reference": " crypto-ref ",
        "eligibility_evidence_present": True,
        "eligibility_evidence_current": True,
        "eligibility_evidence_sufficient": True,
        "eligibility_evidence_contradictory": False,
        "crypto_eligible": False,
        "crypto_excluded": False,
        "crypto_restricted": False,
        "eligibility_evidence_reference": " evidence-ref ",
        "correlation_reference": " correlation-ref ",
    }
    values.update(changes)
    return values


def request(**changes: object) -> CryptoEligibilityRequest:
    values = required_values(
        crypto_lane_confirmation=CryptoLaneConfirmation.CONFIRMED,
    )
    values.update(changes)
    return create_request(**values)


def generic(**changes: object) -> GenericAssetClassContext:
    values: dict[str, object] = {
        "asset_class": AssetClass.CRYPTO,
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
        "reason_code": ReasonCode.CRYPTO_ELIGIBLE,
        "required_action": RequiredAction.NONE,
        "crypto_reference": "crypto-ref",
        "eligibility_evidence_reference": "evidence-ref",
        "correlation_reference": "correlation-ref",
    }
    values.update(changes)
    return Decision(**values)


class AlternateAuthority:
    validity = Validity.VALID
    current = True
    revoked = False
    contradictory = False
    in_scope = True
    evidence_reference = "alternate-authority"


class AlternateGenericContext:
    asset_class = AssetClass.CRYPTO
    validity = Validity.VALID
    current = True
    contradictory = False
    in_scope = True
    context_reference = "alternate-context"


class CryptoEligibilityExclusionTests(unittest.TestCase):
    def assert_mapping(
        self,
        value: CryptoEligibilityRequest,
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
            "CryptoEligibilityRequest",
            "CryptoLaneConfirmation",
            "Validity",
            "create_request",
            "evaluate",
        ])
        expected = {
            AssetClass: ["STOCK", "OPTIONS", "CRYPTO"],
            CryptoLaneConfirmation: ["CONFIRMED", "NOT_CONFIRMED", "CONTRADICTORY"],
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
                "CRYPTO_ELIGIBLE",
                "CRYPTO_EXCLUDED",
                "CRYPTO_RESTRICTED",
                "CRYPTO_ELIGIBILITY_EVIDENCE_MISSING",
                "CRYPTO_ELIGIBILITY_EVIDENCE_STALE",
                "CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT",
                "CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY",
                "CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT",
                "CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT",
                "CRYPTO_LANE_CONFIRMATION_MISSING",
                "CRYPTO_LANE_NOT_CONFIRMED",
                "CRYPTO_LANE_CONTRADICTORY",
                "GENERIC_ASSET_CLASS_CONTEXT_INVALID",
                "GENERIC_ASSET_CLASS_CONTEXT_STALE",
                "GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY",
                "GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE",
                "GENERIC_ASSET_CLASS_NOT_CRYPTO",
                "AUTHORITY_EVIDENCE_INVALID",
                "AUTHORITY_EVIDENCE_STALE",
                "AUTHORITY_EVIDENCE_REVOKED",
                "AUTHORITY_EVIDENCE_OUT_OF_SCOPE",
                "UNDEFINED_INPUT_COMBINATION",
                "CRYPTO_ELIGIBILITY_UNRESOLVED",
            ],
        }
        for enum_type, values in expected.items():
            with self.subTest(enum=enum_type.__name__):
                self.assertEqual([member.name for member in enum_type], values)
                self.assertEqual([member.value for member in enum_type], values)
                self.assertEqual(len(enum_type.__members__), len(list(enum_type)))
                self.assertTrue(issubclass(enum_type, str))
        self.assertEqual(len(Outcome), 4)
        self.assertEqual(len(ReasonCode), 23)
        self.assertEqual(len(RequiredAction), 5)
        for enum_type in expected:
            with self.subTest(unknown_enum=enum_type.__name__):
                with self.assertRaises(ValueError):
                    enum_type("UNKNOWN")
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
            CryptoEligibilityRequest: [
                ("crypto_reference", str),
                ("eligibility_evidence_present", bool),
                ("eligibility_evidence_current", bool),
                ("eligibility_evidence_sufficient", bool),
                ("eligibility_evidence_contradictory", bool),
                ("crypto_eligible", bool),
                ("crypto_excluded", bool),
                ("crypto_restricted", bool),
                ("eligibility_evidence_reference", str),
                ("correlation_reference", str),
                ("crypto_lane_confirmation", CryptoLaneConfirmation | None),
                ("generic_asset_class_context", GenericAssetClassContext | None),
                ("authority_evidence", AuthorityEvidence | None),
            ],
            Decision: [
                ("outcome", Outcome),
                ("reason_code", ReasonCode),
                ("required_action", RequiredAction),
                ("crypto_reference", str),
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
                self.assertTrue(dataclass_type.__dataclass_params__.eq)
                self.assertTrue(all(
                    field.default_factory is dataclasses.MISSING
                    for field in actual_fields
                ))
        request_fields = dataclasses.fields(CryptoEligibilityRequest)
        self.assertTrue(all(
            field.default is dataclasses.MISSING for field in request_fields[:10]
        ))
        self.assertTrue(all(field.default is None for field in request_fields[10:]))
        for dataclass_type in (GenericAssetClassContext, AuthorityEvidence, Decision):
            self.assertTrue(all(
                field.default is dataclasses.MISSING
                for field in dataclasses.fields(dataclass_type)
            ))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            request().crypto_reference = "changed"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            generic().current = False
        with self.assertRaises(dataclasses.FrozenInstanceError):
            authority().revoked = True
        with self.assertRaises(dataclasses.FrozenInstanceError):
            decision().outcome = Outcome.EXCLUDED

    def test_all_frozen_dataclasses_have_governed_value_equality(self) -> None:
        cases = (
            (GenericAssetClassContext, generic(), generic(), generic(current=False)),
            (AuthorityEvidence, authority(), authority(), authority(revoked=True)),
            (
                CryptoEligibilityRequest,
                request(),
                request(),
                request(crypto_eligible=True),
            ),
            (
                Decision,
                decision(),
                decision(),
                decision(crypto_reference="changed-crypto-reference"),
            ),
        )
        for dataclass_type, first, second, changed in cases:
            with self.subTest(dataclass=dataclass_type.__name__):
                self.assertIs(dataclass_type.__dataclass_params__.eq, True)
                self.assertEqual(first, second)
                self.assertIsNot(first, second)
                self.assertNotEqual(first, changed)

    def test_exact_function_signatures(self) -> None:
        create_signature = inspect.signature(create_request)
        self.assertEqual(list(create_signature.parameters), ["values"])
        self.assertIs(
            create_signature.parameters["values"].kind,
            inspect.Parameter.VAR_KEYWORD,
        )
        create_annotations = inspect.get_annotations(create_request, eval_str=True)
        self.assertIs(create_annotations["values"], object)
        self.assertIs(create_annotations["return"], CryptoEligibilityRequest)
        evaluate_signature = inspect.signature(evaluate)
        self.assertEqual(list(evaluate_signature.parameters), ["request"])
        self.assertIs(
            evaluate_signature.parameters["request"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        evaluate_annotations = inspect.get_annotations(evaluate, eval_str=True)
        self.assertIs(evaluate_annotations["request"], CryptoEligibilityRequest)
        self.assertIs(evaluate_annotations["return"], Decision)

    def test_omission_and_explicit_none_boundaries(self) -> None:
        omitted = create_request(**required_values())
        self.assertIsNone(omitted.crypto_lane_confirmation)
        self.assertIsNone(omitted.generic_asset_class_context)
        self.assertIsNone(omitted.authority_evidence)
        explicit_lane_none = create_request(**required_values(
            crypto_lane_confirmation=None,
        ))
        self.assertIsNone(explicit_lane_none.crypto_lane_confirmation)
        with self.assertRaises(TypeError):
            create_request(**required_values(generic_asset_class_context=None))
        with self.assertRaises(TypeError):
            create_request(**required_values(authority_evidence=None))
        direct = CryptoEligibilityRequest(**required_values())
        self.assertIsNone(direct.crypto_lane_confirmation)
        self.assertIsNone(direct.generic_asset_class_context)
        self.assertIsNone(direct.authority_evidence)
        direct_explicit_none = CryptoEligibilityRequest(**required_values(
            crypto_lane_confirmation=None,
            generic_asset_class_context=None,
            authority_evidence=None,
        ))
        self.assertIsNone(direct_explicit_none.crypto_lane_confirmation)
        self.assertIsNone(direct_explicit_none.generic_asset_class_context)
        self.assertIsNone(direct_explicit_none.authority_evidence)

    def test_missing_extra_positional_and_request_boolean_boundaries(self) -> None:
        for field in REQUIRED_REQUEST_FIELDS:
            values = required_values()
            del values[field]
            with self.subTest(missing=field), self.assertRaises(TypeError):
                create_request(**values)
        with self.assertRaises(TypeError):
            create_request(**required_values(extra=True))
        with self.assertRaises(TypeError):
            create_request("positional")  # type: ignore[call-arg]
        boolean_fields = [
            "eligibility_evidence_present",
            "eligibility_evidence_current",
            "eligibility_evidence_sufficient",
            "eligibility_evidence_contradictory",
            "crypto_eligible",
            "crypto_excluded",
            "crypto_restricted",
        ]
        for field, wrong in itertools.product(
            boolean_fields,
            (0, 1, "true", None, [], (), {}),
        ):
            with self.subTest(field=field, wrong=wrong), self.assertRaises(TypeError):
                create_request(**required_values(**{field: wrong}))

    def test_nested_fields_are_required_and_strict(self) -> None:
        generic_values: dict[str, object] = {
            "asset_class": AssetClass.CRYPTO,
            "validity": Validity.VALID,
            "current": True,
            "contradictory": False,
            "in_scope": True,
            "context_reference": "generic-ref",
        }
        authority_values: dict[str, object] = {
            "validity": Validity.VALID,
            "current": True,
            "revoked": False,
            "contradictory": False,
            "in_scope": True,
            "evidence_reference": "authority-ref",
        }
        for constructor, values in (
            (GenericAssetClassContext, generic_values),
            (AuthorityEvidence, authority_values),
        ):
            for field in values:
                incomplete = dict(values)
                del incomplete[field]
                with self.subTest(type=constructor.__name__, missing=field):
                    with self.assertRaises(TypeError):
                        constructor(**incomplete)
        wrong_scalars = (0, 1, "true", None, [], (), {})
        for field, wrong in itertools.product(
            ("current", "contradictory", "in_scope"),
            wrong_scalars,
        ):
            with self.subTest(generic_bool=field, wrong=wrong):
                with self.assertRaises(TypeError):
                    generic(**{field: wrong})
        for field, wrong in itertools.product(
            ("current", "revoked", "contradictory", "in_scope"),
            wrong_scalars,
        ):
            with self.subTest(authority_bool=field, wrong=wrong):
                with self.assertRaises(TypeError):
                    authority(**{field: wrong})
        for field, wrong_values in (
            (
                "asset_class",
                ("CRYPTO", 1, True, None, [], (), {}, deferral.AssetClass.CRYPTO),
            ),
            (
                "validity",
                (
                    "VALID",
                    1,
                    True,
                    None,
                    [],
                    (),
                    {},
                    stock_eligibility.Validity.VALID,
                ),
            ),
        ):
            for wrong in wrong_values:
                with self.subTest(generic_enum=field, wrong=wrong):
                    with self.assertRaises(TypeError):
                        generic(**{field: wrong})
        for wrong in (
            "VALID",
            1,
            True,
            None,
            [],
            (),
            {},
            stock_eligibility.Validity.VALID,
        ):
            with self.subTest(authority_validity=wrong):
                with self.assertRaises(TypeError):
                    authority(validity=wrong)
        for wrong in (
            "CONFIRMED",
            1,
            True,
            [],
            (),
            {},
            deferral.CryptoLaneConfirmation.CONFIRMED,
        ):
            with self.subTest(lane_confirmation=wrong):
                with self.assertRaises(TypeError):
                    request(crypto_lane_confirmation=wrong)

    def test_alternate_subclass_and_deferral_shapes_are_rejected(self) -> None:
        class AuthoritySubclass(AuthorityEvidence):
            pass

        class GenericSubclass(GenericAssetClassContext):
            pass

        class RequestSubclass(CryptoEligibilityRequest):
            pass

        authority_subclass = AuthoritySubclass(
            Validity.VALID, True, False, False, True, "authority-subclass"
        )
        generic_subclass = GenericSubclass(
            AssetClass.CRYPTO, Validity.VALID, True, False, True, "generic-subclass"
        )
        deferral_authority = deferral.AuthorityEvidence(
            "VALID", True, False, False, True, "deferral-authority"
        )
        deferral_generic = deferral.GenericAssetClassContext(
            deferral.AssetClass.CRYPTO,
            "VALID",
            True,
            False,
            True,
            "deferral-generic",
        )
        asset_class_authority = asset_class_eligibility.AuthorityEvidence(
            asset_class_eligibility.Validity.VALID,
            True,
            False,
            False,
            True,
            "asset-class-authority",
        )
        options_authority = options_eligibility.AuthorityEvidence(
            options_eligibility.Validity.VALID,
            True,
            False,
            False,
            True,
            "options-authority",
        )
        stock_authority = stock_eligibility.AuthorityEvidence(
            stock_eligibility.Validity.VALID,
            True,
            False,
            False,
            True,
            "stock-authority",
        )
        stock_generic = stock_eligibility.GenericAssetClassContext(
            stock_eligibility.AssetClass.CRYPTO,
            stock_eligibility.Validity.VALID,
            True,
            False,
            True,
            "stock-generic",
        )
        for wrong in (
            {},
            AlternateAuthority(),
            authority_subclass,
            deferral_authority,
            asset_class_authority,
            options_authority,
            stock_authority,
        ):
            with self.subTest(authority_type=type(wrong).__name__):
                with self.assertRaises(TypeError):
                    request(authority_evidence=wrong)
        for wrong in (
            {},
            AlternateGenericContext(),
            generic_subclass,
            deferral_generic,
            stock_generic,
        ):
            with self.subTest(generic_type=type(wrong).__name__):
                with self.assertRaises(TypeError):
                    request(generic_asset_class_context=wrong)
        subclass_request = RequestSubclass(**required_values(
            crypto_lane_confirmation=CryptoLaneConfirmation.CONFIRMED,
        ))
        with self.assertRaises(TypeError):
            evaluate(subclass_request)

    def test_reference_type_content_identity_and_preservation_boundaries(self) -> None:
        for field in (
            "crypto_reference",
            "eligibility_evidence_reference",
            "correlation_reference",
        ):
            for wrong in (None, 1, True, object(), [], (), {}):
                with self.subTest(field=field, wrong=wrong):
                    with self.assertRaises(TypeError):
                        create_request(**required_values(**{field: wrong}))
            for wrong in ("", " ", "\t\n"):
                with self.subTest(field=field, blank=repr(wrong)):
                    with self.assertRaises(ValueError):
                        create_request(**required_values(**{field: wrong}))
        for constructor, field in (
            (generic, "context_reference"),
            (authority, "evidence_reference"),
        ):
            for wrong in (None, 1, True, object(), [], (), {}):
                with self.subTest(nested_reference=field, wrong=wrong):
                    with self.assertRaises(TypeError):
                        constructor(**{field: wrong})
            with self.assertRaises(ValueError):
                constructor(**{field: "   "})
        crypto_reference = "".join(("  crypto", " exact  "))
        evidence_reference = "".join(("  evidence", " exact  "))
        correlation_reference = "".join(("  correlation", " exact  "))
        context = generic(context_reference="  generic exact  ")
        evidence = authority(evidence_reference="  authority exact  ")
        value = request(
            crypto_reference=crypto_reference,
            eligibility_evidence_reference=evidence_reference,
            correlation_reference=correlation_reference,
            crypto_eligible=True,
            generic_asset_class_context=context,
            authority_evidence=evidence,
        )
        result = evaluate(value)
        self.assertIs(value.crypto_reference, crypto_reference)
        self.assertIs(value.eligibility_evidence_reference, evidence_reference)
        self.assertIs(value.correlation_reference, correlation_reference)
        self.assertIs(value.generic_asset_class_context, context)
        self.assertIs(value.authority_evidence, evidence)
        self.assertIs(result.crypto_reference, crypto_reference)
        self.assertIs(result.eligibility_evidence_reference, evidence_reference)
        self.assertIs(result.correlation_reference, correlation_reference)

    def test_decision_action_and_evaluate_type_boundaries(self) -> None:
        for field, wrong_values in (
            ("outcome", ("ELIGIBLE", 1, True, None, [], (), {})),
            ("reason_code", ("CRYPTO_ELIGIBLE", 1, True, None, [], (), {})),
            ("required_action", ("NONE", 1, True, None, [], (), {})),
        ):
            for wrong in wrong_values:
                with self.subTest(field=field, wrong=wrong):
                    with self.assertRaises(TypeError):
                        decision(**{field: wrong})
        for action in (
            RequiredAction.FOUNDER_AUTHORITY_REQUIRED,
            RequiredAction.RESET_REQUIRED,
        ):
            with self.subTest(action=action), self.assertRaises(ValueError):
                decision(required_action=action)
        for action in (
            RequiredAction.NONE,
            RequiredAction.HUMAN_REVIEW,
            RequiredAction.GOVERNANCE_REVIEW,
        ):
            self.assertEqual(decision(required_action=action).required_action, action)
        for field in (
            "crypto_reference",
            "eligibility_evidence_reference",
            "correlation_reference",
        ):
            for wrong in (None, 1, True, object(), [], (), {}):
                with self.subTest(decision_reference=field, wrong=wrong):
                    with self.assertRaises(TypeError):
                        decision(**{field: wrong})
                with self.assertRaises(ValueError):
                    decision(**{field: "   "})
        deferral_request = deferral.create_request(
            crypto_reference="deferral-request",
            crypto_evidence_present=True,
            crypto_evidence_current=True,
            crypto_evidence_sufficient=True,
            crypto_evidence_contradictory=False,
            crypto_deferral=False,
            crypto_no_action=False,
            crypto_restricted=False,
            crypto_excluded=False,
            correlation_reference="deferral-correlation",
            crypto_lane_confirmation=deferral.CryptoLaneConfirmation.CONFIRMED,
        )
        for wrong in (None, {}, object(), "request", deferral_request):
            with self.subTest(evaluate_type=type(wrong).__name__):
                with self.assertRaises(TypeError):
                    evaluate(wrong)  # type: ignore[arg-type]

    def test_all_sixteen_branches_and_exact_mappings(self) -> None:
        generic_failure = generic(contradictory=True)
        authority_failure = authority(revoked=True)
        cases = (
            (
                "evidence contradiction",
                request(
                    eligibility_evidence_contradictory=True,
                    crypto_eligible=True,
                    crypto_excluded=True,
                    crypto_restricted=True,
                    crypto_lane_confirmation=None,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW),
            ),
            (
                "eligible excluded conflict",
                request(
                    crypto_eligible=True,
                    crypto_excluded=True,
                    crypto_restricted=True,
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=True,
                    crypto_lane_confirmation=None,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "eligible restricted conflict",
                request(
                    crypto_eligible=True,
                    crypto_restricted=True,
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=True,
                    crypto_lane_confirmation=None,
                ),
                (Outcome.RESTRICTED, ReasonCode.CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW),
            ),
            (
                "undefined",
                request(
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=True,
                    eligibility_evidence_sufficient=False,
                    crypto_lane_confirmation=None,
                    crypto_excluded=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "lane missing",
                request(
                    crypto_lane_confirmation=None,
                    generic_asset_class_context=generic_failure,
                    crypto_excluded=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "lane contradictory",
                request(
                    crypto_lane_confirmation=CryptoLaneConfirmation.CONTRADICTORY,
                    generic_asset_class_context=generic_failure,
                    crypto_excluded=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_LANE_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "lane not confirmed",
                request(
                    crypto_lane_confirmation=CryptoLaneConfirmation.NOT_CONFIRMED,
                    generic_asset_class_context=generic_failure,
                    crypto_excluded=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_LANE_NOT_CONFIRMED, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "generic context",
                request(
                    generic_asset_class_context=generic_failure,
                    crypto_excluded=True,
                    authority_evidence=authority_failure,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "excluded",
                request(
                    crypto_excluded=True,
                    crypto_restricted=True,
                    authority_evidence=authority_failure,
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=False,
                    eligibility_evidence_sufficient=False,
                ),
                (Outcome.EXCLUDED, ReasonCode.CRYPTO_EXCLUDED, RequiredAction.NONE),
            ),
            (
                "restricted",
                request(
                    crypto_restricted=True,
                    authority_evidence=authority_failure,
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=False,
                    eligibility_evidence_sufficient=False,
                ),
                (Outcome.RESTRICTED, ReasonCode.CRYPTO_RESTRICTED, RequiredAction.HUMAN_REVIEW),
            ),
            (
                "authority",
                request(
                    authority_evidence=authority_failure,
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=False,
                    eligibility_evidence_sufficient=False,
                    crypto_eligible=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.AUTHORITY_EVIDENCE_REVOKED, RequiredAction.GOVERNANCE_REVIEW),
            ),
            (
                "evidence missing",
                request(
                    eligibility_evidence_present=False,
                    eligibility_evidence_current=False,
                    eligibility_evidence_sufficient=False,
                    crypto_eligible=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW),
            ),
            (
                "evidence stale",
                request(
                    eligibility_evidence_current=False,
                    eligibility_evidence_sufficient=False,
                    crypto_eligible=True,
                ),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW),
            ),
            (
                "evidence insufficient",
                request(eligibility_evidence_sufficient=False, crypto_eligible=True),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW),
            ),
            (
                "eligible",
                request(crypto_eligible=True),
                (Outcome.ELIGIBLE, ReasonCode.CRYPTO_ELIGIBLE, RequiredAction.NONE),
            ),
            (
                "fallback",
                request(),
                (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW),
            ),
        )
        self.assertEqual(len(cases), 16)
        for name, value, expected in cases:
            with self.subTest(branch=name):
                self.assert_mapping(value, expected)

    def test_all_postures_and_governed_undefined_predicates(self) -> None:
        posture_mappings = {
            (False, False, False): (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW),
            (False, False, True): (Outcome.RESTRICTED, ReasonCode.CRYPTO_RESTRICTED, RequiredAction.HUMAN_REVIEW),
            (False, True, False): (Outcome.EXCLUDED, ReasonCode.CRYPTO_EXCLUDED, RequiredAction.NONE),
            (False, True, True): (Outcome.EXCLUDED, ReasonCode.CRYPTO_EXCLUDED, RequiredAction.NONE),
            (True, False, False): (Outcome.ELIGIBLE, ReasonCode.CRYPTO_ELIGIBLE, RequiredAction.NONE),
            (True, False, True): (Outcome.RESTRICTED, ReasonCode.CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW),
            (True, True, False): (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            (True, True, True): (Outcome.REVIEW_REQUIRED, ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
        }
        for posture, expected in posture_mappings.items():
            with self.subTest(posture=posture):
                self.assert_mapping(request(
                    crypto_eligible=posture[0],
                    crypto_excluded=posture[1],
                    crypto_restricted=posture[2],
                ), expected)
        undefined_states = (
            {"eligibility_evidence_present": False, "eligibility_evidence_current": True, "eligibility_evidence_sufficient": False},
            {"eligibility_evidence_present": False, "eligibility_evidence_current": False, "eligibility_evidence_sufficient": True},
            {"eligibility_evidence_present": True, "eligibility_evidence_current": False, "eligibility_evidence_sufficient": True},
        )
        self.assertEqual(len(undefined_states), 3)
        for state in undefined_states:
            with self.subTest(undefined=state):
                self.assert_mapping(request(**state), (
                    Outcome.REVIEW_REQUIRED,
                    ReasonCode.UNDEFINED_INPUT_COMBINATION,
                    RequiredAction.GOVERNANCE_REVIEW,
                ))
                self.assert_mapping(request(crypto_excluded=True, **state), (
                    Outcome.REVIEW_REQUIRED,
                    ReasonCode.UNDEFINED_INPUT_COMBINATION,
                    RequiredAction.GOVERNANCE_REVIEW,
                ))
                self.assert_mapping(request(
                    eligibility_evidence_contradictory=True,
                    **state,
                ), (
                    Outcome.REVIEW_REQUIRED,
                    ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY,
                    RequiredAction.HUMAN_REVIEW,
                ))

    def test_constructible_adjacent_and_multi_condition_precedence_collisions(self) -> None:
        generic_failure = generic(contradictory=True)
        authority_failure = authority(contradictory=True)
        cases = (
            (request(eligibility_evidence_contradictory=True, crypto_eligible=True, crypto_excluded=True), ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY),
            (request(crypto_eligible=True, crypto_excluded=True, crypto_restricted=True), ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT),
            (request(crypto_eligible=True, crypto_restricted=True, eligibility_evidence_present=False, eligibility_evidence_current=True), ReasonCode.CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT),
            (request(eligibility_evidence_present=False, eligibility_evidence_current=True, crypto_lane_confirmation=None), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (request(crypto_lane_confirmation=None, generic_asset_class_context=generic_failure), ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING),
            (request(crypto_lane_confirmation=CryptoLaneConfirmation.NOT_CONFIRMED, generic_asset_class_context=generic_failure), ReasonCode.CRYPTO_LANE_NOT_CONFIRMED),
            (request(generic_asset_class_context=generic_failure, crypto_excluded=True), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY),
            (request(crypto_excluded=True, crypto_restricted=True), ReasonCode.CRYPTO_EXCLUDED),
            (request(crypto_restricted=True, authority_evidence=authority_failure), ReasonCode.CRYPTO_RESTRICTED),
            (request(authority_evidence=authority_failure, eligibility_evidence_present=False, eligibility_evidence_current=False, eligibility_evidence_sufficient=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (request(eligibility_evidence_present=False, eligibility_evidence_current=False, eligibility_evidence_sufficient=False), ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_MISSING),
            (request(eligibility_evidence_current=False, eligibility_evidence_sufficient=False), ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_STALE),
            (request(eligibility_evidence_sufficient=False, crypto_eligible=True), ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT),
        )
        for value, reason in cases:
            with self.subTest(winner=reason):
                self.assertIs(evaluate(value).reason_code, reason)

    def test_generic_states_and_all_fourteen_pairwise_collisions(self) -> None:
        states = [
            "contradictory",
            "ambiguous",
            "invalid",
            "not_crypto",
            "stale",
            "out_of_scope",
        ]
        reason_by_state = {
            "contradictory": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY,
            "ambiguous": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID,
            "invalid": ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID,
            "not_crypto": ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO,
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
                asset_class=(
                    AssetClass.STOCK if "not_crypto" in active else AssetClass.CRYPTO
                ),
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
                self.assert_mapping(
                    request(generic_asset_class_context=build(set(pair))),
                    (
                        Outcome.REVIEW_REQUIRED,
                        reason_by_state[winner],
                        RequiredAction.GOVERNANCE_REVIEW,
                    ),
                )

    def test_authority_states_and_all_fourteen_pairwise_collisions(self) -> None:
        states = [
            "contradictory",
            "ambiguous",
            "invalid",
            "revoked",
            "stale",
            "out_of_scope",
        ]
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
        self.assert_mapping(request(
            authority_evidence=authority(in_scope=False),
            eligibility_evidence_present=False,
            eligibility_evidence_current=False,
            eligibility_evidence_sufficient=False,
            crypto_eligible=True,
        ), (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE,
            RequiredAction.GOVERNANCE_REVIEW,
        ))

    def test_all_reason_and_required_action_mappings_are_covered(self) -> None:
        representatives = {
            ReasonCode.CRYPTO_ELIGIBLE: request(crypto_eligible=True),
            ReasonCode.CRYPTO_EXCLUDED: request(crypto_excluded=True),
            ReasonCode.CRYPTO_RESTRICTED: request(crypto_restricted=True),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_MISSING: request(eligibility_evidence_present=False, eligibility_evidence_current=False, eligibility_evidence_sufficient=False),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_STALE: request(eligibility_evidence_current=False, eligibility_evidence_sufficient=False),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT: request(eligibility_evidence_sufficient=False),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY: request(eligibility_evidence_contradictory=True),
            ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT: request(crypto_eligible=True, crypto_excluded=True),
            ReasonCode.CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT: request(crypto_eligible=True, crypto_restricted=True),
            ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING: request(crypto_lane_confirmation=None),
            ReasonCode.CRYPTO_LANE_NOT_CONFIRMED: request(crypto_lane_confirmation=CryptoLaneConfirmation.NOT_CONFIRMED),
            ReasonCode.CRYPTO_LANE_CONTRADICTORY: request(crypto_lane_confirmation=CryptoLaneConfirmation.CONTRADICTORY),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID: request(generic_asset_class_context=generic(validity=Validity.INVALID)),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE: request(generic_asset_class_context=generic(current=False)),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY: request(generic_asset_class_context=generic(contradictory=True)),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE: request(generic_asset_class_context=generic(in_scope=False)),
            ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO: request(generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS)),
            ReasonCode.AUTHORITY_EVIDENCE_INVALID: request(authority_evidence=authority(validity=Validity.INVALID)),
            ReasonCode.AUTHORITY_EVIDENCE_STALE: request(authority_evidence=authority(current=False)),
            ReasonCode.AUTHORITY_EVIDENCE_REVOKED: request(authority_evidence=authority(revoked=True)),
            ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE: request(authority_evidence=authority(in_scope=False)),
            ReasonCode.UNDEFINED_INPUT_COMBINATION: request(eligibility_evidence_present=False, eligibility_evidence_current=True),
            ReasonCode.CRYPTO_ELIGIBILITY_UNRESOLVED: request(),
        }
        expected_mapping = {
            ReasonCode.CRYPTO_ELIGIBLE: (Outcome.ELIGIBLE, RequiredAction.NONE),
            ReasonCode.CRYPTO_EXCLUDED: (Outcome.EXCLUDED, RequiredAction.NONE),
            ReasonCode.CRYPTO_RESTRICTED: (Outcome.RESTRICTED, RequiredAction.HUMAN_REVIEW),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_MISSING: (Outcome.REVIEW_REQUIRED, RequiredAction.HUMAN_REVIEW),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_STALE: (Outcome.REVIEW_REQUIRED, RequiredAction.HUMAN_REVIEW),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT: (Outcome.REVIEW_REQUIRED, RequiredAction.HUMAN_REVIEW),
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY: (Outcome.REVIEW_REQUIRED, RequiredAction.HUMAN_REVIEW),
            ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT: (Outcome.RESTRICTED, RequiredAction.HUMAN_REVIEW),
            ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.CRYPTO_LANE_NOT_CONFIRMED: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.CRYPTO_LANE_CONTRADICTORY: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.AUTHORITY_EVIDENCE_INVALID: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.AUTHORITY_EVIDENCE_STALE: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.AUTHORITY_EVIDENCE_REVOKED: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.UNDEFINED_INPUT_COMBINATION: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
            ReasonCode.CRYPTO_ELIGIBILITY_UNRESOLVED: (Outcome.REVIEW_REQUIRED, RequiredAction.GOVERNANCE_REVIEW),
        }
        self.assertEqual(set(representatives), set(ReasonCode))
        self.assertEqual(set(expected_mapping), set(ReasonCode))
        emitted_actions: set[RequiredAction] = set()
        for reason, value in representatives.items():
            with self.subTest(reason=reason):
                result = evaluate(value)
                self.assertIs(result.reason_code, reason)
                self.assertEqual(
                    (result.outcome, result.required_action),
                    expected_mapping[reason],
                )
                emitted_actions.add(result.required_action)
        self.assertEqual(emitted_actions, {
            RequiredAction.NONE,
            RequiredAction.HUMAN_REVIEW,
            RequiredAction.GOVERNANCE_REVIEW,
        })
        self.assertNotIn(RequiredAction.FOUNDER_AUTHORITY_REQUIRED, emitted_actions)
        self.assertNotIn(RequiredAction.RESET_REQUIRED, emitted_actions)

    def test_absent_and_valid_contexts_continue_without_granting_eligibility(self) -> None:
        unresolved = (
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_ELIGIBILITY_UNRESOLVED,
            RequiredAction.GOVERNANCE_REVIEW,
        )
        self.assert_mapping(request(), unresolved)
        self.assert_mapping(request(generic_asset_class_context=generic()), unresolved)
        self.assert_mapping(request(authority_evidence=authority()), unresolved)
        self.assert_mapping(request(
            generic_asset_class_context=generic(),
            authority_evidence=authority(),
        ), unresolved)

    def test_reference_preservation_purity_nonmutation_and_repetition(self) -> None:
        context = generic(context_reference="  generic exact  ")
        evidence = authority(evidence_reference="  authority exact  ")
        value = request(
            crypto_reference="  crypto exact  ",
            eligibility_evidence_reference="  eligibility exact  ",
            correlation_reference="  correlation exact  ",
            crypto_eligible=True,
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
        self.assertEqual(first.crypto_reference, value.crypto_reference)
        self.assertEqual(
            first.eligibility_evidence_reference,
            value.eligibility_evidence_reference,
        )
        self.assertEqual(first.correlation_reference, value.correlation_reference)
        self.assertEqual(context.context_reference, "  generic exact  ")
        self.assertEqual(evidence.evidence_reference, "  authority exact  ")

    def test_schema_api_parity_and_founder_trace(self) -> None:
        schema = json.loads(Path(
            "schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json"
        ).read_text(encoding="utf-8"))
        definitions = schema["$defs"]
        self.assertEqual(
            schema["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )
        self.assertEqual(
            schema["$id"],
            "https://echoauth.local/schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json",
        )
        self.assertEqual(schema["required"], ["request", "decision"])
        self.assertEqual(list(schema["properties"]), ["request", "decision"])
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(list(definitions), [
            "AssetClass",
            "CryptoLaneConfirmation",
            "Validity",
            "Outcome",
            "ReasonCode",
            "RequiredAction",
            "GenericAssetClassContext",
            "AuthorityEvidence",
            "Request",
            "Decision",
        ])
        for enum_type, definition in (
            (AssetClass, "AssetClass"),
            (CryptoLaneConfirmation, "CryptoLaneConfirmation"),
            (Validity, "Validity"),
            (Outcome, "Outcome"),
            (ReasonCode, "ReasonCode"),
            (RequiredAction, "RequiredAction"),
        ):
            self.assertEqual(
                [member.value for member in enum_type],
                definitions[definition]["enum"],
            )
        for dataclass_type, definition in (
            (GenericAssetClassContext, "GenericAssetClassContext"),
            (AuthorityEvidence, "AuthorityEvidence"),
            (CryptoEligibilityRequest, "Request"),
            (Decision, "Decision"),
        ):
            field_names = [field.name for field in dataclasses.fields(dataclass_type)]
            self.assertEqual(field_names, list(definitions[definition]["properties"]))
            self.assertFalse(definitions[definition]["additionalProperties"])
            if definition != "Request":
                self.assertEqual(definitions[definition]["required"], field_names)
        self.assertEqual(definitions["Request"]["required"], REQUIRED_REQUEST_FIELDS)
        self.assertEqual(
            definitions["Request"]["properties"]["crypto_lane_confirmation"]["oneOf"],
            [{"$ref": "#/$defs/CryptoLaneConfirmation"}, {"type": "null"}],
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
            definitions["Decision"]["properties"]["required_action"]["allOf"][1]["enum"],
            ["NONE", "HUMAN_REVIEW", "GOVERNANCE_REVIEW"],
        )
        for definition, names in (
            ("Request", [
                "eligibility_evidence_present",
                "eligibility_evidence_current",
                "eligibility_evidence_sufficient",
                "eligibility_evidence_contradictory",
                "crypto_eligible",
                "crypto_excluded",
                "crypto_restricted",
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
                "crypto_reference",
                "eligibility_evidence_reference",
                "correlation_reference",
            ]),
            ("GenericAssetClassContext", ["context_reference"]),
            ("AuthorityEvidence", ["evidence_reference"]),
            ("Decision", [
                "crypto_reference",
                "eligibility_evidence_reference",
                "correlation_reference",
            ]),
        ):
            for name in names:
                reference_schema = definitions[definition]["properties"][name]
                self.assertEqual(reference_schema["type"], "string")
                self.assertEqual(reference_schema["minLength"], 1)
                self.assertEqual(reference_schema["pattern"], "\\S")
        covered: set[int] = set()
        for start, end in re.findall(
            r"\b(\d{2})(?:-(\d{2}))?\b",
            schema["$comment"],
        ):
            lower = int(start)
            upper = int(end) if end else lower
            covered.update(range(lower, upper + 1))
        self.assertEqual(covered, set(range(1, 73)))
        prohibited_context_properties = {
            "venue",
            "exchange",
            "network",
            "bridge",
            "stablecoin",
            "wallet",
            "custody",
            "defi",
            "smart_contract",
            "liquidity",
            "volatility",
            "tokenomics",
            "jurisdiction",
            "regulation",
            "sanctions",
            "platform_policy",
            "account",
            "balance",
            "margin",
            "collateral",
            "leverage",
            "liquidation",
            "risk",
            "sizing",
            "strategy",
            "signal",
            "routing",
            "order",
            "execution",
        }
        self.assertFalse(
            prohibited_context_properties & set(definitions["Request"]["properties"])
        )

    def test_package_root_remains_crypto_deferral_only(self) -> None:
        expected = [
            "AssetClass",
            "AuthorityEvidence",
            "Decision",
            "EmittableReasonCode",
            "GenericAssetClassContext",
            "CryptoLaneConfirmation",
            "CryptoRequest",
            "Outcome",
            "ReasonCode",
            "RequiredAction",
            "create_request",
            "evaluate",
        ]
        self.assertEqual(crypto_package.__all__, expected)
        self.assertIs(crypto_package.AssetClass, deferral.AssetClass)
        self.assertIs(crypto_package.Decision, deferral.Decision)
        self.assertIs(crypto_package.create_request, deferral.create_request)
        self.assertIsNot(crypto_package.AssetClass, AssetClass)
        self.assertNotIn("CryptoEligibilityRequest", crypto_package.__all__)
        self.assertNotIn("Validity", crypto_package.__all__)
        initializer = Path("src/sniperbot/crypto/__init__.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("eligibility_decision", initializer)
        self.assertNotIn("CryptoEligibilityRequest", initializer)

    def test_production_import_and_prohibited_capability_boundary(self) -> None:
        source = Path(
            "src/sniperbot/crypto/eligibility_decision.py"
        ).read_text(encoding="utf-8")
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
            "exchange",
            "broker",
            "wallet",
            "custody",
            "blockchain",
            "market_data",
            "sanctions",
            "account",
            "balance",
            "risk",
            "sizing",
            "routing",
            "order",
            "execution",
        }
        used_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        self.assertFalse(used_names & prohibited_names)
        self.assertFalse(any(
            isinstance(node, (ast.AsyncFunctionDef, ast.Await))
            for node in ast.walk(tree)
        ))
        self.assertFalse(any(
            isinstance(node, (ast.Global, ast.Nonlocal, ast.Delete, ast.Yield, ast.YieldFrom))
            for node in ast.walk(tree)
        ))
        self.assertNotIn("sniperbot.crypto.deferral_decision", source)
        self.assertNotIn("TODO", source)
        self.assertNotIn("NotImplementedError", source)


if __name__ == "__main__":
    unittest.main()
