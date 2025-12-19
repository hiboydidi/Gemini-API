# Fly.io 部署指南

## 前置要求

1. 安装 [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/)
2. 登录 Fly.io 账户：
   ```bash
   flyctl auth login
   ```

## 配置说明

### 1. 设置 Secrets（必需）

在部署前，需要设置 Gemini cookies 作为 secrets：

```bash
flyctl secrets set GEMINI_COOKIE_1PSID="g.a0004gj80Jqx-HKUQLVSg237tV5I99tHU2N5u9umX2T9caFsaC0JXQoFj_fkeJ66oCw13SHKtAACgYKATMSARQSFQHGX2MivlCwL1eNBfxtzCAwZ80QaBoVAUF8yKrf9Kjq6SvvXNzHb-qyIVgn0076" -a gemini-api-1tbpvg

flyctl secrets set GEMINI_COOKIE_1PSIDTS="sidts-CjIBflaCdcd1sj8KjunC7Vv6DGB77gl3Beh7UflQpNNxX4EYeIS21l6lNbiUnRJpoN9UsBAA" -a gemini-api-1tbpvg
```

### 2. 创建持久化卷（可选但推荐）

用于存储自动刷新的 cookies：

```bash
flyctl volumes create gemini_data --region hkg --size 1 -a gemini-api-1tbpvg
```

## 部署步骤

### 首次部署

```bash
flyctl deploy -a gemini-api-1tbpvg
```

### 更新部署

```bash
flyctl deploy -a gemini-api-1tbpvg
```

## 常用命令

### 查看应用状态
```bash
flyctl status -a gemini-api-1tbpvg
```

### 查看日志
```bash
flyctl logs -a gemini-api-1tbpvg
```

### 查看实时日志
```bash
flyctl logs -a gemini-api-1tbpvg -f
```

### SSH 进入容器
```bash
flyctl ssh console -a gemini-api-1tbpvg
```

### 查看 Secrets
```bash
flyctl secrets list -a gemini-api-1tbpvg
```

### 更新 Secrets
```bash
flyctl secrets set GEMINI_COOKIE_1PSID="新的cookie值" -a gemini-api-1tbpvg
```

### 查看卷状态
```bash
flyctl volumes list -a gemini-api-1tbpvg
```

## 配置文件说明

### `Dockerfile`
- 基于 Python 3.11-slim 镜像
- 安装项目依赖
- 暴露 8000 端口
- Cookie 存储路径：`/data/gemini_webapi`

### `fly.toml`
- **app**: 应用名称 `gemini-api-1tbpvg`
- **primary_region**: 主要区域 `hkg`（香港）
- **internal_port**: 内部端口 8000
- **memory**: 1GB RAM
- **cpus**: 1 个共享 CPU
- **auto_stop_machines**: 自动停止闲置机器（节省费用）
- **mounts**: 挂载持久化卷到 `/data`

## 环境变量

| 变量名 | 说明 | 设置方式 |
|--------|------|----------|
| `GEMINI_COOKIE_PATH` | Cookie 存储路径 | fly.toml 中配置 |
| `GEMINI_COOKIE_1PSID` | Google 认证 cookie | flyctl secrets |
| `GEMINI_COOKIE_1PSIDTS` | Google 认证时间戳 | flyctl secrets |

## 故障排查

### 1. 部署失败：Dockerfile 错误
确保项目根目录存在 `Dockerfile` 文件，而不是使用 `docker-compose.yml`

### 2. Cookie 未持久化
检查卷是否正确创建和挂载：
```bash
flyctl volumes list -a gemini-api-1tbpvg
flyctl ssh console -a gemini-api-1tbpvg
ls -la /data/gemini_webapi
```

### 3. 应用无法访问
检查应用状态和日志：
```bash
flyctl status -a gemini-api-1tbpvg
flyctl logs -a gemini-api-1tbpvg
```

### 4. Cookie 过期
更新 secrets：
```bash
flyctl secrets set GEMINI_COOKIE_1PSID="新值" -a gemini-api-1tbpvg
flyctl secrets set GEMINI_COOKIE_1PSIDTS="新值" -a gemini-api-1tbpvg
```

### 5. 内存不足
增加 VM 内存（需要修改 fly.toml）：
```toml
[[vm]]
  memory = '2gb'  # 从 1gb 增加到 2gb
```

然后重新部署：
```bash
flyctl deploy -a gemini-api-1tbpvg
```

## 费用优化

- **auto_stop_machines**: 设置为 `stop` 可在无请求时自动停止机器
- **min_machines_running**: 设置为 `0` 允许完全停止
- **持久化卷**: 1GB 卷每月约 $0.15

## 访问应用

部署成功后，应用将可通过以下地址访问：
```
https://gemini-api-1tbpvg.fly.dev
```

## 注意事项

1. ⚠️ **Secrets 安全**：不要将 cookies 提交到 Git，始终使用 `flyctl secrets`
2. 📦 **持久化**：使用卷挂载确保 cookies 在重启后保留
3. 💰 **费用**：注意监控使用量，合理配置自动停止策略
4. 🔄 **Cookie 刷新**：应用会自动刷新 cookies 并保存到 `/data` 目录
