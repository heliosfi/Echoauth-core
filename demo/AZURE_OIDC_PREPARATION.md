# EchoAuth OIDC preparation — HOLD / NOT CONNECTED

Authority: N.B.C. Preparation and verification only. No merge, deployment,
production CI/CD activation, production configuration change, or live runtime authority.

## Observed evidence (2026-10-20 America/New_York)

- Draft PR #46 inspected at head `82d8a82edc5f426067b3c676968a19d64ad6302a`.
- That head's demo verification run 39527742589 and Authority Clarity run
  39527742500 previously returned success. These are not Azure federation tests.
- Azure portal sign-in verified with MFA in Default Directory.
- Tenant: `134573e7-3bc7-44bb-9cc5-1092f76d5573`.
- Subscription: `981ad91c-4948-4573-926d-ddfeca224b84`.
- Resource group AND App Service name: `echoauth-core-rg`.
- Exact target resource:
  `/subscriptions/981ad91c-4948-4573-926d-ddfeca224b84/resourceGroups/echoauth-core-rg/providers/Microsoft.Web/sites/echoauth-core-rg`.
- App Service IAM showed two inherited Owner entries for the signed-in user;
  no service principal or managed identity role assignment was displayed.
  This does not establish absence of identities elsewhere in the tenant.
- Deployment Center showed the production slot, GitHub as selected source,
  and an Authorize button. No Save, Authorize, or Sync was invoked.
  The displayed selection alone does not prove an active source connection.

## Proposed trust configuration (NOT APPLIED)

Use a dedicated user-assigned managed identity, proposed name
`echoauth-github-verify`, with no client secret or publish profile.
Do not attach it to the production application's runtime identity.

The following federated credential is a preparation example only. First verify
the repository's effective OIDC subject format; a customized subject may differ.
Do not create this credential until the protected environment exists and all
checks below pass.

```json
{
  "name": "echoauth-github-verification",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:heliosfi/Echoauth-core:environment:echoauth-azure-verification",
  "audiences": ["api://AzureADTokenExchange"]
}
```

For the first verification phase, propose Reader ONLY at the exact App Service
resource scope above. Do not grant Contributor, Owner, subscription-wide access,
Website Contributor, or role-assignment permissions to the verification identity.
A future deployment identity and its write permissions require a separate,
reviewable approval; verification identity access does not authorize deployment.

Record the actual client ID and principal ID only after identity creation is
approved and verified. Neither ID is currently established. Tenant, subscription,
and client IDs are configuration identifiers, not stored client secrets.

## GitHub gate prerequisites (NOT VERIFIED / NOT CREATED)

- Repository must be exactly `heliosfi/Echoauth-core`.
- Environment must be exactly `echoauth-azure-verification`.
- Verify repository plan supports enforceable environment protections. If it
  does not, HOLD rather than silently remove the gate.
- Require the designated N.B.C. reviewer, disallow administrative bypass where
  supported, and restrict eligible deployment branches to an explicitly
  approved branch. Do not allow wildcard branches or tags.
- Verify the effective repository OIDC subject template and exact environment
  subject, including case.
- An environment subject does not bind a branch by itself. Enforce branch
  restrictions in the environment and workflow together.
- Before publishing any runnable workflow, review the full resulting diff,
  exact action commit pins and upstream provenance, environment rules, and
  identity/RBAC receipt.

## Future read-only verification workflow contract (NOT INSTALLED)

Keep all preparation outside `.github/workflows`. This document creates no
runnable workflow and requests no OIDC tokens.

A separately approved verification workflow must:
1. Offer manual dispatch only, with no push, pull_request, pull_request_target,
   schedule, workflow_run, or reusable-workflow trigger.
2. Fail before token issuance unless the repository, event, approved ref,
   approved source commit, target tenant/subscription/resource, environment,
   and nonempty configuration values match the reviewed receipt.
3. Grant contents: read by default and id-token: write only to the gated OIDC
   job. Do not grant repository write permissions.
4. Use the protected environment above. Pin every action to a verified full
   commit SHA; leave activation blocked if pins are unverified.
5. Use Azure Login OIDC with the verified client ID, tenant ID, subscription ID,
   and audience api://AzureADTokenExchange. Never use a client secret or
   publish profile as a fallback.
6. Read account tenant/subscription and the exact App Service resource ID,
   name, type, and resource group; compare them to this receipt and fail on
   any mismatch. Avoid listing app settings, credentials, or access tokens.
7. Perform no deployment, source-control configuration, role assignment,
   app-setting update, startup update, restart, slot swap, or content upload.
8. Log out and preserve a nonsensitive verification receipt. Success proves
   only bounded read access, not authority to deploy or authorize requests.

## Stop conditions and current disposition

HOLD / NOT CONNECTED. Identity/client ID, effective GitHub OIDC subject,
protected environment support/rules, least-privilege RBAC, action pins, and
actual token exchange remain unverified. No live connection is claimed.

Do not activate trust, grant access, publish a runnable OIDC workflow, merge
PR #46, or save Deployment Center production settings while those checks are
incomplete. Browser access grants require confirmation at the point of action.
Separate N.B.C. approval remains necessary for production changes/deployment.

Preserve the existing demo behavior: POST /api/v1/authorize returns HTTP 503,
decision HOLD, authorized false. Federation does not supply runtime authority.

## Primary references

- https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions
- https://docs.github.com/en/actions/reference/security/oidc
- https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
