import ast
import inspect
import json
import unittest
from dataclasses import MISSING, FrozenInstanceError, fields
from pathlib import Path

import sniperbot.eligibility as eligibility
from sniperbot.eligibility.asset_class_decision import (
    AssetClass, AuthorityEvidence, Decision, EligibilityRequest, Outcome,
    ReasonCode, RequiredAction, Validity, create_request, evaluate,
)


def authority(**overrides):
    values = dict(validity=Validity.VALID, current=True, revoked=False,
                  contradictory=False, in_scope=True,
                  evidence_reference="authority-1")
    values.update(overrides)
    return AuthorityEvidence(**values)


def request(**overrides):
    values = dict(
        asset_class=AssetClass.STOCK,
        eligibility_reference="eligibility-1",
        eligibility_evidence_present=True,
        eligibility_evidence_current=True,
        eligibility_evidence_sufficient=True,
        eligibility_evidence_contradictory=False,
        asset_class_eligible=False,
        asset_class_excluded=False,
        asset_class_restricted=False,
        correlation_reference="correlation-1",
    )
    values.update(overrides)
    return EligibilityRequest(**values)


class AlternateDeferralAuthority:
    def __init__(self):
        self.validity = "VALID"
        self.currentness = "CURRENT"
        self.revocation = "NON_REVOKED"
        self.scope = "IN_SCOPE"
        self.evidence_reference = "alternate-authority"


class AssetClassEligibilityExclusionTests(unittest.TestCase):
    def assert_mapping(self, result, outcome, reason, action):
        self.assertEqual((result.outcome, result.reason_code, result.required_action),
                         (outcome, reason, action))

    def test_exact_public_api(self):
        expected = ["AssetClass", "Outcome", "ReasonCode", "RequiredAction",
                    "Validity", "AuthorityEvidence", "EligibilityRequest",
                    "Decision", "create_request", "evaluate"]
        self.assertEqual(eligibility.__all__, expected)
        self.assertEqual(len(eligibility.__all__), len(set(eligibility.__all__)))
        for name in expected:
            self.assertTrue(hasattr(eligibility, name))
        self.assertFalse(hasattr(eligibility, "EmittableAction"))

    def test_schema_and_dataclass_parity(self):
        schema = json.loads(Path("schemas/sniperbot-asset-class-eligibility-exclusion-decision.schema.json").read_text(encoding="utf-8"))
        defs = schema["$defs"]
        for enum_type, name in [(AssetClass, "AssetClass"), (Outcome, "Outcome"),
                                (ReasonCode, "ReasonCode"),
                                (RequiredAction, "RequiredAction"),
                                (Validity, "Validity")]:
            self.assertEqual([member.value for member in enum_type], defs[name]["enum"])
        self.assertEqual([field.name for field in fields(AuthorityEvidence)], list(defs["AuthorityEvidence"]["properties"]))
        self.assertEqual([field.name for field in fields(EligibilityRequest)], list(defs["Request"]["required"]) + ["authority_evidence"])
        self.assertEqual([field.name for field in fields(Decision)], list(defs["Decision"]["required"]))

    def test_vocabularies_and_non_emittable_actions(self):
        self.assertEqual((len(AssetClass), len(Outcome), len(ReasonCode),
                          len(RequiredAction), len(Validity)), (3, 4, 15, 5, 3))
        base = dict(asset_class=AssetClass.STOCK,
                    eligibility_reference="eligibility-1",
                    outcome=Outcome.ELIGIBLE,
                    reason_code=ReasonCode.ASSET_CLASS_ELIGIBLE,
                    correlation_reference="correlation-1")
        for action in [RequiredAction.FOUNDER_AUTHORITY_REQUIRED,
                       RequiredAction.RESET_REQUIRED]:
            with self.assertRaises(ValueError):
                Decision(required_action=action, **base)

    def test_enum_members_have_no_hidden_aliases(self):
        expected = {
            AssetClass: ["STOCK", "OPTIONS", "CRYPTO"],
            Outcome: ["ELIGIBLE", "EXCLUDED", "RESTRICTED", "REVIEW_REQUIRED"],
            ReasonCode: [
                "ASSET_CLASS_ELIGIBLE", "ASSET_CLASS_EXCLUDED",
                "ASSET_CLASS_RESTRICTED", "ELIGIBILITY_EVIDENCE_MISSING",
                "ELIGIBILITY_EVIDENCE_STALE", "ELIGIBILITY_EVIDENCE_INSUFFICIENT",
                "ELIGIBILITY_EVIDENCE_CONTRADICTORY", "ELIGIBLE_EXCLUDED_CONFLICT",
                "ELIGIBLE_RESTRICTED_CONFLICT", "AUTHORITY_EVIDENCE_INVALID",
                "AUTHORITY_EVIDENCE_STALE", "AUTHORITY_EVIDENCE_REVOKED",
                "AUTHORITY_EVIDENCE_OUT_OF_SCOPE", "UNDEFINED_INPUT_COMBINATION",
                "ELIGIBILITY_UNRESOLVED",
            ],
            RequiredAction: ["NONE", "HUMAN_REVIEW", "GOVERNANCE_REVIEW",
                             "FOUNDER_AUTHORITY_REQUIRED", "RESET_REQUIRED"],
            Validity: ["VALID", "INVALID", "AMBIGUOUS"],
        }
        for enum_type, names in expected.items():
            with self.subTest(enum=enum_type.__name__):
                self.assertEqual(list(enum_type.__members__), names)
                self.assertEqual(len(enum_type.__members__), len(names))
                self.assertNotIn("UNKNOWN", enum_type.__members__)
                self.assertEqual(len({member.value for member in enum_type.__members__.values()}), len(names))
                for name in names:
                    self.assertIs(enum_type.__members__[name], getattr(enum_type, name))

    def test_authority_fields_are_all_required_without_defaults(self):
        expected = ["validity", "current", "revoked", "contradictory",
                    "in_scope", "evidence_reference"]
        definitions = list(fields(AuthorityEvidence))
        self.assertEqual([field.name for field in definitions], expected)
        for field in definitions:
            self.assertIs(field.default, MISSING)
            self.assertIs(field.default_factory, MISSING)
        valid = dict(validity=Validity.VALID, current=True, revoked=False,
                     contradictory=False, in_scope=True,
                     evidence_reference="authority-1")
        for name in expected:
            values = valid.copy()
            values.pop(name)
            with self.subTest(missing=name):
                with self.assertRaises(TypeError):
                    AuthorityEvidence(**values)

    def test_alternate_deferral_authority_shapes_are_rejected(self):
        with self.assertRaises(TypeError):
            request(authority_evidence=AlternateDeferralAuthority())
        alternate = dict(validity="VALID", currentness="CURRENT",
                         revocation="NON_REVOKED", scope="IN_SCOPE",
                         evidence_reference="alternate-authority")
        with self.assertRaises(TypeError):
            request(authority_evidence=alternate)

    def test_raw_decision_enum_strings_are_type_errors(self):
        valid = dict(asset_class=AssetClass.STOCK,
                     eligibility_reference="eligibility-1",
                     outcome=Outcome.ELIGIBLE,
                     reason_code=ReasonCode.ASSET_CLASS_ELIGIBLE,
                     required_action=RequiredAction.NONE,
                     correlation_reference="correlation-1")
        for field, raw in [("outcome", "ELIGIBLE"),
                           ("reason_code", "ASSET_CLASS_ELIGIBLE"),
                           ("required_action", "NONE")]:
            values = valid.copy()
            values[field] = raw
            with self.subTest(field=field):
                with self.assertRaises(TypeError):
                    Decision(**values)

    def test_boolean_fields_are_strict(self):
        request_fields = ["eligibility_evidence_present",
                          "eligibility_evidence_current",
                          "eligibility_evidence_sufficient",
                          "eligibility_evidence_contradictory",
                          "asset_class_eligible", "asset_class_excluded",
                          "asset_class_restricted"]
        authority_fields = ["current", "revoked", "contradictory", "in_scope"]
        invalid = [0, 1, "true", None, [], {}, object()]
        for field in request_fields:
            for value in invalid:
                with self.subTest(field=field, value=repr(value)):
                    with self.assertRaises(TypeError):
                        request(**{field: value})
        for field in authority_fields:
            for value in invalid:
                with self.subTest(field=field, value=repr(value)):
                    with self.assertRaises(TypeError):
                        authority(**{field: value})

    def test_enum_nested_keyword_and_evaluate_type_validation(self):
        with self.assertRaises(TypeError):
            request(asset_class="STOCK")
        with self.assertRaises(TypeError):
            authority(validity="VALID")
        for value in [{}, object(), "authority", 1]:
            with self.assertRaises(TypeError):
                request(authority_evidence=value)
        with self.assertRaises(TypeError):
            create_request(**self._request_values(authority_evidence=None))
        with self.assertRaises(TypeError):
            create_request(**self._request_values(unexpected=True))
        for value in [None, {}, object(), "request"]:
            with self.assertRaises(TypeError):
                evaluate(value)

    def test_reference_validation(self):
        with self.assertRaises(ValueError):
            request(eligibility_reference="")
        with self.assertRaises(ValueError):
            request(correlation_reference="")
        with self.assertRaises(ValueError):
            authority(evidence_reference="")
        base = dict(asset_class=AssetClass.STOCK, outcome=Outcome.ELIGIBLE,
                    reason_code=ReasonCode.ASSET_CLASS_ELIGIBLE,
                    required_action=RequiredAction.NONE)
        with self.assertRaises(ValueError):
            Decision(eligibility_reference="", correlation_reference="x", **base)
        with self.assertRaises(ValueError):
            Decision(eligibility_reference="x", correlation_reference="", **base)

    def test_immutability(self):
        for obj, field in [(authority(), "current"), (request(), "asset_class_eligible"),
                           (evaluate(request()), "outcome")]:
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, None)

    def test_all_twelve_branches_and_mappings(self):
        cases = [
            (dict(eligibility_evidence_contradictory=True), Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW),
            (dict(asset_class_eligible=True, asset_class_excluded=True), Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            (dict(asset_class_eligible=True, asset_class_restricted=True), Outcome.RESTRICTED, ReasonCode.ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW),
            (dict(eligibility_evidence_present=False, eligibility_evidence_current=True), Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            (dict(asset_class_excluded=True), Outcome.EXCLUDED, ReasonCode.ASSET_CLASS_EXCLUDED, RequiredAction.NONE),
            (dict(asset_class_restricted=True), Outcome.RESTRICTED, ReasonCode.ASSET_CLASS_RESTRICTED, RequiredAction.HUMAN_REVIEW),
            (dict(authority_evidence=authority(validity=Validity.INVALID)), Outcome.REVIEW_REQUIRED, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW),
            (dict(eligibility_evidence_present=False, eligibility_evidence_current=False, eligibility_evidence_sufficient=False), Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW),
            (dict(eligibility_evidence_current=False, eligibility_evidence_sufficient=False), Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW),
            (dict(eligibility_evidence_sufficient=False), Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW),
            (dict(asset_class_eligible=True), Outcome.ELIGIBLE, ReasonCode.ASSET_CLASS_ELIGIBLE, RequiredAction.NONE),
            ({}, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW),
        ]
        for overrides, outcome, reason, action in cases:
            with self.subTest(reason=reason):
                self.assert_mapping(evaluate(request(**overrides)), outcome, reason, action)

    def test_exactly_three_undefined_predicates(self):
        cases = [
            dict(eligibility_evidence_present=False, eligibility_evidence_current=True),
            dict(eligibility_evidence_present=False, eligibility_evidence_sufficient=True),
            dict(eligibility_evidence_current=False, eligibility_evidence_sufficient=True),
        ]
        for overrides in cases:
            self.assertEqual(evaluate(request(**overrides)).reason_code,
                             ReasonCode.UNDEFINED_INPUT_COMBINATION)
        self.assertEqual(evaluate(request()).reason_code, ReasonCode.ELIGIBILITY_UNRESOLVED)

    def test_conflicts_win_over_each_undefined_predicate(self):
        undefined = [
            dict(eligibility_evidence_present=False,
                 eligibility_evidence_current=True,
                 eligibility_evidence_sufficient=False),
            dict(eligibility_evidence_present=False,
                 eligibility_evidence_current=False,
                 eligibility_evidence_sufficient=True),
            dict(eligibility_evidence_present=True,
                 eligibility_evidence_current=False,
                 eligibility_evidence_sufficient=True),
        ]
        conflicts = [
            (dict(asset_class_eligible=True, asset_class_excluded=True),
             Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBLE_EXCLUDED_CONFLICT,
             RequiredAction.GOVERNANCE_REVIEW),
            (dict(asset_class_eligible=True, asset_class_restricted=True),
             Outcome.RESTRICTED, ReasonCode.ELIGIBLE_RESTRICTED_CONFLICT,
             RequiredAction.HUMAN_REVIEW),
        ]
        for posture, outcome, reason, action in conflicts:
            for index, predicate in enumerate(undefined, 1):
                values = predicate | posture
                with self.subTest(conflict=reason, predicate=index):
                    self.assert_mapping(evaluate(request(**values)), outcome, reason, action)
        all_three = request(asset_class_eligible=True, asset_class_excluded=True,
                            asset_class_restricted=True)
        self.assertEqual(evaluate(all_three).reason_code,
                         ReasonCode.ELIGIBLE_EXCLUDED_CONFLICT)

    def test_undefined_category_wins_over_each_compatible_lower_category(self):
        witnesses = [
            ("missing", dict(eligibility_evidence_present=False,
                             eligibility_evidence_current=True,
                             eligibility_evidence_sufficient=False)),
            ("stale", dict(eligibility_evidence_present=True,
                           eligibility_evidence_current=False,
                           eligibility_evidence_sufficient=True)),
            # P1 necessarily includes missing while proving undefined over insufficient.
            ("insufficient", dict(eligibility_evidence_present=False,
                                  eligibility_evidence_current=True,
                                  eligibility_evidence_sufficient=False)),
            ("exclusion", dict(eligibility_evidence_present=False,
                               eligibility_evidence_current=True,
                               eligibility_evidence_sufficient=False,
                               asset_class_excluded=True)),
            ("restriction", dict(eligibility_evidence_present=False,
                                 eligibility_evidence_current=True,
                                 eligibility_evidence_sufficient=False,
                                 asset_class_restricted=True)),
            ("authority", dict(eligibility_evidence_present=False,
                               eligibility_evidence_current=True,
                               eligibility_evidence_sufficient=False,
                               authority_evidence=authority(validity=Validity.INVALID))),
            ("eligible", dict(eligibility_evidence_present=False,
                              eligibility_evidence_current=True,
                              eligibility_evidence_sufficient=False,
                              asset_class_eligible=True)),
            ("fallback", dict(eligibility_evidence_present=False,
                              eligibility_evidence_current=True,
                              eligibility_evidence_sufficient=False)),
        ]
        for lower, values in witnesses:
            with self.subTest(lower=lower):
                self.assert_mapping(evaluate(request(**values)), Outcome.REVIEW_REQUIRED,
                                    ReasonCode.UNDEFINED_INPUT_COMBINATION,
                                    RequiredAction.GOVERNANCE_REVIEW)

    def test_exclusion_wins_over_every_compatible_lower_category(self):
        lower_cases = [("restriction", dict(asset_class_restricted=True))]
        lower_cases += [(f"authority-{name}", dict(authority_evidence=authority(**values)))
                        for name, values, _ in self._authority_failures()]
        lower_cases += [
            ("missing", dict(eligibility_evidence_present=False,
                             eligibility_evidence_current=False,
                             eligibility_evidence_sufficient=False)),
            ("stale", dict(eligibility_evidence_current=False,
                           eligibility_evidence_sufficient=False)),
            ("insufficient", dict(eligibility_evidence_sufficient=False)),
            ("fallback", {}),
        ]
        for lower, values in lower_cases:
            with self.subTest(lower=lower):
                self.assert_mapping(evaluate(request(asset_class_excluded=True, **values)),
                                    Outcome.EXCLUDED, ReasonCode.ASSET_CLASS_EXCLUDED,
                                    RequiredAction.NONE)

    def test_restriction_wins_over_every_compatible_lower_category(self):
        lower_cases = [(f"authority-{name}", dict(authority_evidence=authority(**values)))
                       for name, values, _ in self._authority_failures()]
        lower_cases += [
            ("missing", dict(eligibility_evidence_present=False,
                             eligibility_evidence_current=False,
                             eligibility_evidence_sufficient=False)),
            ("stale", dict(eligibility_evidence_current=False,
                           eligibility_evidence_sufficient=False)),
            ("insufficient", dict(eligibility_evidence_sufficient=False)),
            ("fallback", {}),
        ]
        for lower, values in lower_cases:
            with self.subTest(lower=lower):
                self.assert_mapping(evaluate(request(asset_class_restricted=True, **values)),
                                    Outcome.RESTRICTED, ReasonCode.ASSET_CLASS_RESTRICTED,
                                    RequiredAction.HUMAN_REVIEW)

    def test_every_authority_failure_wins_over_all_lower_categories(self):
        lower_cases = [
            ("missing", dict(eligibility_evidence_present=False,
                             eligibility_evidence_current=False,
                             eligibility_evidence_sufficient=False)),
            ("stale", dict(eligibility_evidence_current=False,
                           eligibility_evidence_sufficient=False)),
            ("insufficient", dict(eligibility_evidence_sufficient=False)),
            ("eligible", dict(asset_class_eligible=True)),
            ("fallback", {}),
        ]
        for authority_name, authority_values, reason in self._authority_failures():
            for lower, request_values in lower_cases:
                with self.subTest(authority=authority_name, lower=lower):
                    result = evaluate(request(
                        authority_evidence=authority(**authority_values),
                        **request_values,
                    ))
                    self.assert_mapping(result, Outcome.REVIEW_REQUIRED, reason,
                                        RequiredAction.GOVERNANCE_REVIEW)

    def test_evidence_ordering_and_eligible_over_fallback(self):
        cases = [
            (dict(eligibility_evidence_present=False,
                  eligibility_evidence_current=False,
                  eligibility_evidence_sufficient=False,
                  asset_class_eligible=True), ReasonCode.ELIGIBILITY_EVIDENCE_MISSING),
            (dict(eligibility_evidence_present=False,
                  eligibility_evidence_current=False,
                  eligibility_evidence_sufficient=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(eligibility_evidence_current=False,
                  eligibility_evidence_sufficient=False,
                  asset_class_eligible=True), ReasonCode.ELIGIBILITY_EVIDENCE_STALE),
            (dict(eligibility_evidence_sufficient=False,
                  asset_class_eligible=True), ReasonCode.ELIGIBILITY_EVIDENCE_INSUFFICIENT),
        ]
        for values, reason in cases:
            with self.subTest(reason=reason):
                self.assertEqual(evaluate(request(**values)).reason_code, reason)
        self.assert_mapping(evaluate(request(asset_class_eligible=True)),
                            Outcome.ELIGIBLE, ReasonCode.ASSET_CLASS_ELIGIBLE,
                            RequiredAction.NONE)
        self.assert_mapping(evaluate(request()), Outcome.REVIEW_REQUIRED,
                            ReasonCode.ELIGIBILITY_UNRESOLVED,
                            RequiredAction.GOVERNANCE_REVIEW)

    def test_authority_failures_and_subprecedence(self):
        cases = [
            (dict(contradictory=True), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(validity=Validity.AMBIGUOUS), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(validity=Validity.INVALID), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(revoked=True), ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            (dict(current=False), ReasonCode.AUTHORITY_EVIDENCE_STALE),
            (dict(in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE),
        ]
        for overrides, reason in cases:
            evidence = authority(**overrides)
            result = evaluate(request(authority_evidence=evidence))
            self.assert_mapping(result, Outcome.REVIEW_REQUIRED, reason,
                                RequiredAction.GOVERNANCE_REVIEW)
        collisions = [
            (dict(contradictory=True, validity=Validity.AMBIGUOUS, revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(validity=Validity.AMBIGUOUS, revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(validity=Validity.INVALID, revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            (dict(current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_STALE),
        ]
        for overrides, reason in collisions:
            self.assertEqual(evaluate(request(authority_evidence=authority(**overrides))).reason_code, reason)

    def test_authority_contradiction_wins_over_invalid_validity(self):
        evidence = AuthorityEvidence(
            validity=Validity.INVALID,
            current=True,
            revoked=False,
            contradictory=True,
            in_scope=True,
            evidence_reference="contradictory-invalid-authority",
        )
        result = evaluate(request(
            authority_evidence=evidence,
            eligibility_evidence_sufficient=False,
            asset_class_eligible=True,
        ))
        self.assert_mapping(
            result,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.AUTHORITY_EVIDENCE_INVALID,
            RequiredAction.GOVERNANCE_REVIEW,
        )

    def test_authority_absent_and_valid_continue(self):
        self.assertEqual(evaluate(request()).reason_code, ReasonCode.ELIGIBILITY_UNRESOLVED)
        self.assertEqual(evaluate(request(authority_evidence=authority())).reason_code,
                         ReasonCode.ELIGIBILITY_UNRESOLVED)
        created = create_request(**self._request_values())
        self.assertIsNone(created.authority_evidence)

    def test_global_precedence_collisions(self):
        low = dict(asset_class_eligible=True, asset_class_excluded=True,
                   asset_class_restricted=True,
                   eligibility_evidence_present=False,
                   eligibility_evidence_current=False,
                   eligibility_evidence_sufficient=False,
                   authority_evidence=authority(validity=Validity.INVALID))
        self.assertEqual(evaluate(request(eligibility_evidence_contradictory=True, **low)).reason_code,
                         ReasonCode.ELIGIBILITY_EVIDENCE_CONTRADICTORY)
        self.assertEqual(evaluate(request(**low)).reason_code, ReasonCode.ELIGIBLE_EXCLUDED_CONFLICT)
        low.pop("asset_class_excluded")
        self.assertEqual(evaluate(request(**low)).reason_code, ReasonCode.ELIGIBLE_RESTRICTED_CONFLICT)
        undefined = dict(eligibility_evidence_present=False,
                         eligibility_evidence_current=True,
                         asset_class_excluded=True, asset_class_restricted=True,
                         authority_evidence=authority(validity=Validity.INVALID))
        self.assertEqual(evaluate(request(**undefined)).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)
        self.assertEqual(evaluate(request(asset_class_excluded=True,
                                          asset_class_restricted=True,
                                          authority_evidence=authority(validity=Validity.INVALID))).reason_code,
                         ReasonCode.ASSET_CLASS_EXCLUDED)
        self.assertEqual(evaluate(request(asset_class_restricted=True,
                                          authority_evidence=authority(validity=Validity.INVALID))).reason_code,
                         ReasonCode.ASSET_CLASS_RESTRICTED)
        self.assertEqual(evaluate(request(authority_evidence=authority(validity=Validity.INVALID),
                                          eligibility_evidence_present=False,
                                          eligibility_evidence_current=False,
                                          eligibility_evidence_sufficient=False)).reason_code,
                         ReasonCode.AUTHORITY_EVIDENCE_INVALID)
        self.assertEqual(evaluate(request(eligibility_evidence_present=False,
                                          eligibility_evidence_current=False,
                                          eligibility_evidence_sufficient=False)).reason_code,
                         ReasonCode.ELIGIBILITY_EVIDENCE_MISSING)
        self.assertEqual(evaluate(request(eligibility_evidence_current=False,
                                          eligibility_evidence_sufficient=False)).reason_code,
                         ReasonCode.ELIGIBILITY_EVIDENCE_STALE)
        self.assertEqual(evaluate(request(eligibility_evidence_sufficient=False,
                                          asset_class_eligible=True)).reason_code,
                         ReasonCode.ELIGIBILITY_EVIDENCE_INSUFFICIENT)
        self.assertEqual(evaluate(request(asset_class_eligible=True)).reason_code,
                         ReasonCode.ASSET_CLASS_ELIGIBLE)

    def test_preservation_nonmutation_and_determinism(self):
        evidence = authority()
        req = request(asset_class=AssetClass.CRYPTO,
                      eligibility_reference="opaque-eligibility",
                      correlation_reference="opaque-correlation",
                      authority_evidence=evidence, asset_class_eligible=True)
        before_request, before_evidence = repr(req), repr(evidence)
        first, second = evaluate(req), evaluate(req)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertIsNot(first, req)
        self.assertEqual((first.asset_class, first.eligibility_reference,
                          first.correlation_reference),
                         (req.asset_class, req.eligibility_reference,
                          req.correlation_reference))
        self.assertEqual((repr(req), repr(evidence)), (before_request, before_evidence))

    def test_production_import_and_capability_boundary(self):
        path = Path("src/sniperbot/eligibility/asset_class_decision.py")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        self.assertEqual(imports, ["__future__", "dataclasses", "enum"])
        source = path.read_text(encoding="utf-8")
        for prohibited in ["sniperbot.deferral", "sniperbot.stock",
                           "sniperbot.options", "sniperbot.crypto",
                           "sniperbot.rollback", "echoauth", "logging",
                           "subprocess", "os.environ", "open(", "socket"]:
            self.assertNotIn(prohibited, source.lower())
        self.assertEqual(inspect.signature(create_request).return_annotation,
                         "EligibilityRequest")

    @staticmethod
    def _request_values(**overrides):
        values = dict(
            asset_class=AssetClass.STOCK,
            eligibility_reference="eligibility-1",
            eligibility_evidence_present=True,
            eligibility_evidence_current=True,
            eligibility_evidence_sufficient=True,
            eligibility_evidence_contradictory=False,
            asset_class_eligible=False,
            asset_class_excluded=False,
            asset_class_restricted=False,
            correlation_reference="correlation-1",
        )
        values.update(overrides)
        return values

    @staticmethod
    def _authority_failures():
        return [
            ("contradictory", dict(contradictory=True),
             ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ("ambiguous", dict(validity=Validity.AMBIGUOUS),
             ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ("invalid", dict(validity=Validity.INVALID),
             ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ("revoked", dict(revoked=True),
             ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            ("stale", dict(current=False),
             ReasonCode.AUTHORITY_EVIDENCE_STALE),
            ("out-of-scope", dict(in_scope=False),
             ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE),
        ]


if __name__ == "__main__":
    unittest.main()
