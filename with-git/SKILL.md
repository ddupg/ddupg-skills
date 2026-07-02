---
name: with-git
description: Use when the user asks to commit, push, publish/open a GitHub PR, submit a community PR, or create a draft PR. Keep git/GitHub publishing on the fast path and match repository style.
---

# With Git

沉淀 git / GitHub 操作里的非默认最佳路径。当前只覆盖 PR 发布收尾里容易走弯路的补充规则，不重复通用 git hygiene。

## PR 发布补充规则

- `git push`、`gh pr create`、必要的 `gh pr view` 直接请求提升权限执行，不先在 sandbox 里试错。
- commit message 和 PR title 都不强制固定格式，但创建前提醒检查目标仓库/社区风格与标题检查要求。
- 默认创建 draft PR，除非用户明确要求 ready PR。
