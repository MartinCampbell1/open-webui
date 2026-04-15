# Auditor Setup

This repository is the live, runnable audit target.

For the other public repositories in this audit pack:

- `UXUI`: public snapshots and manifests only, no login required
- `HermesUI`: public docs and reference material only, no login required
- `hermes-ui-audit-pack`: public audit bundle/archive only, no login required

Only a running `open-webui` instance needs authentication.

## Recommended Branch

For the current Hermes/OpenWebUI UX/UI audit, use:

```bash
git checkout codex/hermes-ui-audit-remediation
```

Useful comparison branches:

- `main`
- `codex/hermes-ui-regression-snapshot-20260411`
- `codex/mmmm`

## Audit Credentials

Use this local audit account for the live UI:

- Email: `test@example.com`
- Password: `test`

This credential is intended for local audit environments only.
Do not expose it on a public deployment.

## Fastest Reproducible Audit Run

This path is the least ambiguous because it runs the exact public branch in an isolated container with a fresh data volume.

```bash
git clone https://github.com/MartinCampbell1/open-webui.git
cd open-webui
git checkout codex/hermes-ui-audit-remediation

docker rm -f open-webui-audit 2>/dev/null || true
docker volume rm open-webui-audit-data 2>/dev/null || true
docker volume create open-webui-audit-data

docker build -t open-webui-audit .

docker run -d \
  --name open-webui-audit \
  -p 3000:8080 \
  -e WEBUI_ADMIN_EMAIL=test@example.com \
  -e WEBUI_ADMIN_PASSWORD=test \
  -e WEBUI_ADMIN_NAME="Audit Test" \
  -v open-webui-audit-data:/app/backend/data \
  open-webui-audit
```

Then open:

- [http://localhost:3000](http://localhost:3000)

And sign in with:

- `test@example.com`
- `test`

## Important Note About Fresh Data

`WEBUI_ADMIN_EMAIL` and `WEBUI_ADMIN_PASSWORD` only create the admin user when the database has no existing users.

If you reuse an old volume or old SQLite database, the automatic admin bootstrap will be skipped.

That is why the commands above explicitly recreate the Docker volume.

## Existing Local Database: Create Or Refresh The Audit User

If you already have a local checkout with an existing SQLite database, run:

```bash
python3 scripts/create_audit_user.py \
  --db backend/open_webui/data/webui.db \
  --email test@example.com \
  --password test \
  --name "Audit Test" \
  --role admin
```

This script upserts the audit user directly in the local SQLite database used by the default repository setup.

## Optional Local Source Run

If you want to run from source instead of Docker, create or refresh the audit user first:

```bash
python3 scripts/create_audit_user.py \
  --db backend/open_webui/data/webui.db \
  --email test@example.com \
  --password test \
  --name "Audit Test" \
  --role admin
```

Then start the backend in your usual local-development way.

One common path in this repository is:

```bash
cd backend
./dev.sh
```

And the frontend:

```bash
npm install
npm run dev
```

If you already use a different local workflow, keep using that workflow. The key point for the auditor is the presence of the same audit account:

- `test@example.com`
- `test`

## What The Auditor Should Review

Primary live target:

- `open-webui` on `codex/hermes-ui-audit-remediation`

Reference repositories:

- `UXUI` for sanitized working-tree snapshots
- `HermesUI` for requirements, context, and historical reference
- `hermes-ui-audit-pack` for the sanitized audit bundle and archive branch

## Public Repository Map

- `open-webui`: live code and runnable UI target
- `UXUI`: public snapshot trees for comparison
- `HermesUI`: public docs/specs/reference pack
- `hermes-ui-audit-pack`: public audit artifacts and sanitized preserve bundle
