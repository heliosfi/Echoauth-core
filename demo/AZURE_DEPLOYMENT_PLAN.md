# EchoAuth demonstration — Azure deployment contract (HOLD)

Authority: N.B.C.  Scope: demonstration only.  Status: NOT DEPLOYED.

## Preconditions
1. N.B.C. separately approves the exact deployment after reviewing verified tests and diff.
2. Confirm Azure subscription, tenant, resource group, App Service name, and Python 3.11 runtime.
3. Establish GitHub OIDC federated credential scoped to the approved repository, branch/environment, and least-privilege Azure identity. Do not use publish profiles or stored client secrets.
4. Protect the GitHub deployment environment with required reviewers and restrict branches.
5. Confirm app's existing files and rollback plan before replacing hostingstart.html.

## Proposed application configuration
Deploy only the contents of demo/ as an artifact. Use startup command:
python echoauth_demo.py

Use App Service's PORT environment variable (or configure PORT=8000 to match the listener). Verify Azure routing and startup before approving release.

## Acceptance checks
GET /api/health returns demo_only, runtime unavailable.
POST /api/v1/authorize returns HTTP 503, HOLD, authorized false.
No endpoint permits a live authorization.
If any test or identity check fails: HOLD. No deployment.

## Boundary
This repository change adds no deploy job, no Azure credentials, no application permissions, and no production runtime implementation. A separate approved change is required before Azure deployment.
