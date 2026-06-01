---
name: with-linear
description: Work from a Linear issue as the source of truth. Use when the user asks to start, continue, fix, implement, investigate, or ship work tied to a Linear issue, or when they explicitly ask to keep Linear status, findings, decisions, or conclusions updated while working.
---

# With Linear

把 Linear issue 当作工作契约；推进任务时，主动维护 issue 状态和关键结论，不等用户反复提醒。

## Workflow

1. 找到并读取目标 issue。
   - 优先使用用户给出的 Linear issue ID 或 URL；没有明确目标时，先从当前上下文推断，仍无法确认再问用户。
   - 开始前读取目标 issue、所属 project 信息、完整父 issue 链和最新评论。
   - project / 父 issue 中的背景、规则、偏好、验收口径和限制，都是当前 issue 的上游上下文。
   - 如果当前 issue 与上游上下文冲突，先指出冲突，不自行猜测。

2. 工作时保持 Linear 可追踪。
   - 在开始、阻塞、关键决策、重要结论、验证完成和收尾时，按需要更新状态或评论。
   - issue 评论只写值得沉淀的状态、证据、结论和后续；不要写成调试流水账。
   - 长报告或会改动 issue 正文/验收标准的内容，先给用户 review；普通阶段性结论仍及时写回 Linear。
   - 向 GitHub PR、GitHub issue、公开 changelog 或其他外部系统提交内容时，不要暴露 Linear issue ID、URL、项目/父 issue、评论、状态或内部决策链；只保留可公开的变更、原因、验证和影响。

3. 写回失败必须显式说明。
   - 如果无法更新 Linear，聊天里写明 `未更新 Linear：<原因>`。
   - 不要声称已经记录或更新。
