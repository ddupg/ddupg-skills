---
name: with-git
description: Use when the user asks to create or work in a git worktree, commit, push, publish/open a GitHub PR, submit a community PR, or create a draft PR. Keep git/GitHub publishing on the fast path and match repository style.
---

# With Git

沉淀 git / GitHub 操作里的非默认最佳路径。不重复通用 git hygiene，只记录容易走弯路的补充规则。

## Worktree 规则

- 默认使用 sibling worktree。

## 分支命名规则

- 新建分支使用 `feat/`、`fix/`、`chore/` 等前缀，不使用 `codex/`。

## PR 发布规则

- 需要写入 Git 元数据或访问远端的 Git/GitHub 命令，直接请求提升权限执行，不先在 sandbox 中尝试。纯本地只读检查按正常权限执行。
- commit message 和 PR title 由目标仓库的现有风格及检查要求决定；创建前自行检查并遵循，不强制统一格式。
- 默认创建 draft PR，除非用户明确要求 ready PR。
