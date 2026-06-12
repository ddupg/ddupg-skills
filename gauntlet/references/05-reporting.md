# 05 Reporting

本阶段生成脱敏的 `report.md` 和 `result.json`。

## 文件布局

```text
.gauntlet/<requirement>/
  run.yaml
  logs/
  report.md
  result.json
```

## 脱敏

报告和日志摘录必须先经过：

```bash
python3 <Gauntlet skill>/scripts/redact-report.py <input> -o <output>
```

或：

```bash
cat <input> | python3 <Gauntlet skill>/scripts/redact-report.py
```

## report.md 必须包含

- 需求和验收标准。
- 本地 repo、同步方式、远端 host、隔离 user、workdir、端口。
- 运行时版本、依赖安装命令、服务启动命令。
- 测试命令、日志路径、关键摘录。
- 失败定位、修复过程、每轮验证结果。
- 最终状态：passed、failed、blocked。
- 未覆盖项和剩余风险。
- 清理命令。默认只给命令，不主动执行。

## result.json 必须包含

- `status`
- `requirement`
- `remote`
- `sync`
- `iterations`
- `commands`
- `logs`
- `fix_summary`
- `evidence`
- `blockers`
- `cleanup`

如果失败或阻塞，`blockers` 必须明确说明缺少什么日志、权限、凭据、复现步骤或文件。
