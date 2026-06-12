# 02 Remote Bootstrap

本阶段用具备 root 权限的 SSH 入口准备远端隔离环境。不要在登录用户或 root 下安装项目依赖、启动项目服务或执行测试。

即使 SSH 登录用户不是 root，只要能通过 `sudo` 或 `su` 获得 root 权限，也必须先创建隔离 user，行为等同 root 登录。只有确认无法创建或切换到隔离 user 时，才允许明确询问用户是否接受在当前登录用户下继续；未获允许前不得污染登录用户 home。

## 资源分配

在远端 root shell 中使用 JSON state 和文件锁分配资源；非 root 登录时先提权：

```bash
python3 <Gauntlet skill>/scripts/alloc-resource.py allocate \
  --state /opt/gauntlet/state/allocations.json \
  --slug "<requirement-slug>" \
  --ports "<port-range>" \
  --port-count "<count>" \
  --work-root "/home"
```

把输出写回 `run.yaml` 的执行记录或报告草稿中：

- `user`
- `workdir`
- `ports`
- `state path`

## Bootstrap

`workdir` 必须是隔离 user 自己的 home，也就是 allocation 输出的 `/home/<allocated-user>`。root 只用于创建用户、安装白名单系统包和设置该 home 目录权限；不要把源码、依赖、日志或运行数据放到 root home，也不要放到共享的 `/home/gauntlet-runs` 目录。

如果允许安装白名单系统包：

```bash
bash <Gauntlet skill>/scripts/bootstrap-remote-user.sh \
  --user "<allocated-user>" \
  --workdir "<allocated-workdir>" \
  --install-base-packages
```

如果不允许安装系统包，去掉 `--install-base-packages`，并检查缺失包。缺失 `git`、`rsync`、`curl`、`tar`、`python3`、构建工具时必须报告阻塞。

## 降权原则

后续命令必须用隔离用户执行。root 登录或可 sudo 的登录用户都优先使用：

```bash
sudo -iu "<allocated-user>" bash -lc '<command>'
```

如果机器没有 `sudo`，使用：

```bash
su - "<allocated-user>" -c '<command>'
```

## Mise

在隔离 user 下安装或启用 `mise`，并按 `project.yaml` / `run.yaml` pin Node/Python 版本。不要污染 root home 或系统级 Node/Python。
