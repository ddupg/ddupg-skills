---
name: next-issue
description: Recommend the user's next tasks using evidence from the current workspace, Linear, GitHub, and other available work sources. Use when the user asks what to work on next or wants help choosing and prioritizing tasks.
---

# Next Issue

Find up to three concrete things the user should consider doing next. Prefer evidence from live sources over memory or guesswork, and keep the result short enough to act on immediately.

## Workflow

1. Identify available sources before asking the user.
   - Use the current conversation and workspace first.
   - Use Linear when available for assigned issues, active cycle items, status, priority, due dates, and blockers.
   - Use GitHub when available for assigned issues, review requests, failing checks, open PRs, and recent mentions.
   - Use local repository context when relevant: `git status`, current branch, recent commits, open TODOs, failing local checks already visible in logs, and nearby issue IDs.
   - Use other explicitly available work sources only when they are already connected or named by the user.

2. Search for actionable candidates.
   - Prefer items assigned to the user, opened or recently touched by the user, blocking another person, failing CI, due soon, or already in progress.
   - Treat stale, ambiguous, or unassigned items as weaker unless they clearly unblock active work.
   - Do not create, update, close, label, or comment on external issues unless the user explicitly asks.

3. Rank candidates by their value in the current situation, respecting the user's stated priorities and available time. Weigh these factors together rather than using a fixed category order:
   - Actual impact and severity, including the scope of production failures, CI failures, or security risks.
   - Urgency, deadlines, and the cost of delay.
   - Dependencies, work unblocked for others, and progress on active commitments.
   - Whether a concrete next action is feasible now, given effort, access, and blockers.

4. Return up to three recommendations by default.
   - If fewer than three actionable candidates are found, return only the candidates with evidence and say which sources were checked.
   - Respect the user's requested count, but do not add unsupported candidates to fill it.
   - If live sources are unavailable, say which sources could not be checked and base the recommendation only on the sources that were actually inspected.

## Output Format

Answer in Chinese by default:

```markdown
建议接下来做这 <N> 件事：

1. <source id/title>
   原因：<1 sentence with source evidence>
   第一步：<one concrete action the user or agent can take now>
2. <source id/title>
   原因：<1 sentence with source evidence>
   第一步：<one concrete action the user or agent can take now>
3. <source id/title>
   原因：<1 sentence with source evidence>
   第一步：<one concrete action the user or agent can take now>

已检查：<sources checked; include unavailable sources briefly>
```

Keep the answer factual. Do not provide a long backlog, broad prioritization essay, or speculative roadmap.
