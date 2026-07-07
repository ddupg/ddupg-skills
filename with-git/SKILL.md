---
name: with-git
description: Use when the user asks to create or work in a git worktree, commit, push, publish/open a GitHub PR, submit a community PR, or create a draft PR. Keep git/GitHub publishing on the fast path and match repository style.
---

# With Git

沉淀 git / GitHub 操作里的非默认最佳路径。不重复通用 git hygiene，只记录容易走弯路的补充规则。

## Worktree 规则

- 创建 worktree 时默认放在原项目同级目录，命名为 `<原项目目录名>.<slug>`；例如 `~/project/lance` -> `~/project/lance.<slug>`。

## PR 发布规则

- `git push`、`gh pr create`、必要的 `gh pr view` 直接请求提升权限执行，不先在 sandbox 里试错。
- commit message 和 PR title 不强制固定格式，但创建前提醒检查目标仓库/社区风格与标题检查要求。
- 默认创建 draft PR，除非用户明确要求 ready PR。
