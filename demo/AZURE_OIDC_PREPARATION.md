# EchoAuth OIDC verification — HOLD / NOT CONNECTED

Authority: N.B.C. authorizes a dedicated OIDC verification identity, Reader
access limited to the App Service, a protected GitHub environment, and a manual
read-only verification workflow. No deployment, merge, production CI/CD
activation, or production application changes.

## Verified Azure target

- Tenant: `134573e7-3bc7-44bb-9cc5-1092f76d5573`.
- Subscription: `981ad91c-4948-4573-926d-ddfeca224b84`.
- Resource group AND App Service name: `echoauth-core-rg`.
- Exact resource:
  `/subscriptions/981ad91c-4948-4573-926d-ddfeca224b84/resourceGroups/echoauth-core-rg/providers/Microsoft.Web/sites/echoauth-core-rg`.
- Azure portal sign-in verified with MFA in Default Directory.
- App Service IAM displayed two inherited Owner entries for the signed-in user,
  and no service-principal or managed-identity role assignment. Identities
  elsewhere in the tenant have not been inventoried.
- Deployment Center showed production, GitHub selected, and an Authorize button.
  No Authorize, Save, or Sync was invoked. This is not proof of a connection.

## GitHub environment created and rules saved

Environment: `echoauth-azure-verification` (ID `24874575619`).

- Required reviewer: `heliosfi` (N.B.C.'s repository account).
- Administrator bypass: disabled.
- Allowed branch ONLY: `demo/bounded-echoauth-azure-20261020`.
- Allowed tags: zero.
- No environment secrets or variables configured.
- Prevent self-review is not enabled: the single authority account may both
  initiate and explicitly approve a verification run. This is a human gate,
  not independent two-person review.

Saved configuration:
https://github.com/heliosfi/Echoauth-core/settings/environments/24874575619/edit

## Manual workflow prepared, NOT RUN

`.github/workflows/echoauth-oidc-readonly.yml` is prepared on PR #46's branch.
It has workflow_dispatch ONLY, an exact repository/ref/job gate, the protected
environment, contents: read, and id-token: write limited to that job.

It uses runner Python standard library directly: no checkout, external action,
client secret, publish profile, Azure CLI cache, or repository script execution.
Before requesting a token it requires environment variables AZURE_CLIENT_ID and
ECHOAUTH_VERIFICATION_SHA, and validates the exact source commit and workflow ref.
It validates the returned GitHub OIDC claims, exchanges the assertion at the
fixed tenant endpoint, then performs only GET against the exact App Service ARM
resource. The sole POST exchanges the token; it is not an Azure resource write.
OAuth responses/tokens are never printed or persisted. Failures return HOLD.

Local checks: YAML parsing, manual-only event, gated environment, minimal job
permissions, embedded Python syntax, and absence of external actions passed.
No live identity or token exchange is verified.

## Concrete execution blocker

GitHub's documentation requires workflow_dispatch workflows to exist on the
default branch for manual triggering. The branch-only demo workflow page was
inspected and has no Run workflow control. Main remains at the existing
95c83e5d5b31acaa92d9fd976162b880cabc1a00 checkpoint.

The current no-merge/no-main-promotion boundary prevents registering this new
manual workflow on main. Do not change the default branch, add automatic
triggers, change an existing default-branch validator, or merge PR #46 to evade
this boundary. A separate approval must identify the exact verification-only
workflow/default-branch registration change before that step is attempted.

https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow

## Azure trust and access — NOT CREATED / NOT GRANTED

Proposed identity: user-assigned managed identity `echoauth-github-verify`.
Do not attach it to the production application's runtime identity.
Client ID and principal ID remain unestablished.

Proposed federated credential (not applied):
```json
{
  "name": "echoauth-github-verification",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:heliosfi/Echoauth-core:environment:echoauth-azure-verification",
  "audiences": ["api://AzureADTokenExchange"]
}
```

Verify the effective repository subject format before creating trust. The
workflow requires this exact subject and fails if a customized format differs.

Grant Reader ONLY at the exact App Service scope above after the manual
execution blocker is resolved and the identity is verified. Never grant this
identity Contributor, Owner, Website Contributor, subscription-wide access,
or role-assignment permissions. Browser access grants require confirmation at
the point of action.

## Disposition

HOLD / NOT CONNECTED. Environment rules are saved; read-only workflow is
prepared but unrun. Azure identity, federation, Reader grant, effective subject
format, and token exchange remain incomplete. Stop before granting unused
access while the execution prerequisite remains unresolved.

Preserve POST /api/v1/authorize -> HTTP 503, HOLD, authorized false.
Federation supplies no runtime authority. Deployment, production changes, and
merge remain separately gated.

## Primary references

- https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions
- https://docs.github.com/en/actions/reference/security/oidc
- https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
