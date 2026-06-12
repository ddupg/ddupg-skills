---
name: gauntlet
description: "Use Gauntlet for real Linux isolated-user integration testing: create .gauntlet YAML contracts, bootstrap remote users, sync local worktrees, run test-and-fix loops, and produce redacted report.md/result.json evidence."
---

# Gauntlet

Gauntlet is a self-contained workflow for validating a development requirement on a real Linux host under an isolated user.

## Skill Root

Resolve `<Gauntlet skill>` as the directory containing this `SKILL.md`.

Bundled resources:

- Main workflow: `references/workflow.md`
- Stage details: `references/01-intake.md` through `references/05-reporting.md`
- Example contracts: `examples/project.yaml` and `examples/run.yaml`
- Helper scripts: `scripts/`
- Report templates: `templates/report.md` and `templates/result.json`

## Workflow

1. Read `references/workflow.md` first.
2. Follow the referenced stages in order.
3. Create or update `.gauntlet/project.yaml` and `.gauntlet/<requirement>/run.yaml` in the business project before any remote command.
4. Use `<Gauntlet skill>/scripts/*` for deterministic helper operations.
5. Write final evidence to `.gauntlet/<requirement>/report.md` and `.gauntlet/<requirement>/result.json`.

## Core Rules

- Investigate discoverable project facts before asking the user.
- Ask only for product intent, credentials, real resources, destructive authorization, or other facts that cannot be discovered locally.
- Real integration tests are the final gate; mocks and unit tests are only supplemental.
- Root privileges are only for remote login or escalation, user bootstrap, whitelisted system package installation, resource allocation, and permissions.
- If the SSH user can gain root via `sudo` or `su`, still bootstrap an isolated user; use the login user only after isolation fails and the user explicitly allows it.
- Dependency installation, services, tests, logs, and data must run under the isolated user home.
- The local business worktree is the source of truth; fix locally, sync remotely, then re-test.
- Do not commit, push, or clean up remote state unless the run contract explicitly says so.
- Redact reports and excerpts before presenting or storing evidence.
