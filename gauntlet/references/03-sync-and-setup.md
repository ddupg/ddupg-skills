# 03 Sync And Setup

本地业务仓库是 source of truth。远端只是运行环境。

## 同步模式

`sync.mode: rsync`:

```bash
bash <Gauntlet skill>/scripts/sync-rsync.sh \
  --source "<local-business-repo>" \
  --target "<ssh-user>@<host>:<allocated-workdir>/repo"
```

用于测试本地未提交改动。

如果 SSH 同步入口不是隔离 user，rsync 目标仍必须在 `<allocated-workdir>` 下；同步后立即用 root 权限修正所有权。下面用 `sudo` 表示提权入口；root 登录时可去掉 `sudo`：

```bash
ssh "<ssh-user>@<host>" \
  'sudo chown -R "<allocated-user>:<allocated-user>" "<allocated-workdir>/repo"'
```

`sync.mode: git`:

```bash
sudo -iu "<allocated-user>" bash -lc '
  mkdir -p "<allocated-workdir>" &&
  cd "<allocated-workdir>" &&
  git clone "<repo-url>" repo &&
  cd repo &&
  git checkout "<branch-or-commit>"
'
```

用于固定 commit 复现。

## 依赖安装

依赖安装命令必须来自 YAML，不允许仅凭猜测执行。常见例子：

远程机器下载依赖很慢时，可以把用户或项目允许的国内源写入 YAML 并在安装命令中使用，例如 npm/pnpm registry 或 pip `-i <mirror>`；不要只在远端临时手改。

```bash
sudo -iu "<allocated-user>" bash -lc '
  cd "<allocated-workdir>/repo" &&
  npm config set registry "<registry>" &&
  pnpm install
'
```

Python 依赖必须安装到隔离 user 的 venv 或项目指定环境，不使用系统 site-packages。

## 服务启动

服务启动命令必须：

- 写入日志文件。
- 记录 PID 或健康检查 URL。
- 使用 YAML 中分配的端口。
- 不占用未分配端口。

启动后必须执行健康检查；健康检查不通过时不要进入测试阶段。
