---
name: with-linear
description: Work from a Linear issue as the source of truth, keeping its status and confirmed conclusions current without logging exploratory discussion.
---

# With Linear

## Workflow

1. 找到并读取目标 issue。
   - 优先使用用户给出的 Linear issue ID 或 URL；没有明确目标时，先从当前上下文推断，仍无法确认再问用户。
   - 开始前读取 issue、所属 project、完整父 issue 链和最新评论；其中的背景、规则、偏好、验收口径和限制都是上游上下文。
   - 如果当前 issue 与上游上下文冲突，先指出冲突，不自行猜测。

2. 工作时保持 Linear 可追踪。
   - 开始时只按需更新状态，不发评论；仅在用户确认讨论结论、出现阻塞、验证完成、收尾或用户明确要求时合并写回。
   - 探索性讨论（包括与 `grilling` 配合）只留在聊天；只记录用户确认的决策和有证据支撑的事实，不记录问题、逐轮回答、候选方案或推测。
   - 首次写回创建一条标记为“with-linear 当前摘要”的精简评论，之后只更新该评论。摘要只保留当前有效的结论、关键证据、未决项和下一步；新结论替换旧结论，变化原因影响后续时才简述。
   - 无法安全更新时不追加，并在聊天里写明 `未更新 Linear：<原因>`，不要声称已记录。
   - 长报告或会改动 issue 正文/验收标准的内容，先给用户 review。
   - 向 GitHub PR、GitHub issue、公开 changelog 或其他外部系统提交内容时，不要暴露 Linear issue ID、URL、项目/父 issue、评论、状态或内部决策链；只保留可公开的变更、原因、验证和影响。
