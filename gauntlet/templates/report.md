# Gauntlet Test Report

## Status

- Result: `<passed|failed|blocked>`
- Requirement: `<title>`
- Run ID: `<run id>`

## Requirement

`<需求描述>`

## Acceptance Criteria

- `<criterion>`

## Environment

- Local repo: `<path>`
- Sync mode: `<rsync|git>`
- Remote host: `<host>`
- Isolated user: `<user>`
- Remote workdir: `<workdir>`
- Ports: `<ports>`
- Runtime: `<node/python versions>`
- External namespace: `<namespace>`

## Commands

| Step | Command | Exit | Log |
| --- | --- | --- | --- |
| setup | `<command>` | `<code>` | `<path>` |
| test | `<command>` | `<code>` | `<path>` |

## Fix Loop

| Iteration | Finding | Local change | Verification |
| --- | --- | --- | --- |
| 1 | `<root cause>` | `<diff summary>` | `<command and result>` |

## Evidence

```text
<redacted key excerpts>
```

## Uncovered Items

- `<item or none>`

## Blockers

- `<missing logs, permissions, credentials, reproduction steps, files, or none>`

## Cleanup

Default cleanup is retain. To release the allocation after review:

```bash
python3 <Gauntlet skill>/scripts/alloc-resource.py release \
  --state /opt/gauntlet/state/allocations.json \
  --user "<user>"
```
