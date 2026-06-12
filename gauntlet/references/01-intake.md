# 01 Intake

本阶段只做调查、追问和 YAML 合同固化，不执行远端命令。

## 输入

- 用户的需求描述。
- Gauntlet skill 路径，也就是包含 `SKILL.md` 的目录。
- 业务项目本地路径。
- 可选的现有 `.gauntlet/project.yaml` 和 `.gauntlet/<requirement>/run.yaml`。

## 调查

先在业务项目中读取：

- README、AGENTS、package/lock files、pyproject、requirements、Makefile、CI workflow、已有测试目录。
- 启动命令、测试命令、端口、环境变量、外部服务配置。
- 是否存在 `.nvmrc`、`.python-version`、`mise.toml`、`volta`、`pnpm-lock.yaml`、`uv.lock` 等版本线索。

## 必须对齐的问题

只问无法从项目读出的内容：

- 需求的真实验收标准是什么。
- 哪些场景必须跑真实集成测试，哪些只能作为 mock/补充测试。
- Linux SSH 入口是什么，登录用户是否可通过 `sudo` 或 `su` 获得 root 权限。
- 是否允许安装白名单系统包。
- 外部服务的测试命名空间是什么，禁止触碰哪些生产资源。
- 需要哪些凭据、registry、proxy、API endpoint；远程下载慢时是否允许使用国内源或镜像。
- 端口、磁盘、并发、运行时长约束。
- 失败后是否允许自动修复。本项目默认允许，但仍需确认是否有高风险文件或目录禁止改动。

## 提问方式

优先使用当前平台的交互式提问工具。一次只问一个问题，并给出推荐选项。

## 输出合同

补齐或创建：

- `.gauntlet/project.yaml`: 项目级 profile。
- `.gauntlet/<requirement>/run.yaml`: 本次需求执行合同。

执行前运行轻量检查：

```bash
python3 <Gauntlet skill>/scripts/validate-config-shape.py project .gauntlet/project.yaml
python3 <Gauntlet skill>/scripts/validate-config-shape.py run .gauntlet/<requirement>/run.yaml
```

轻量检查通过不代表可以跳过人工语义核对；agent 必须确认 YAML 中的命令、资源、凭据和测试命名空间都与用户意图一致。
