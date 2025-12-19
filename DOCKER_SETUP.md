# Docker 部署配置说明

## 配置完成 ✅

已为您配置好 Gemini WebAPI 的 Docker 持久化部署方案。

## 文件说明

### 1. `docker-compose.yml`
Docker Compose 配置文件，已配置：
- Cookie 持久化路径：`/tmp/gemini_webapi`
- 卷映射：`./gemini_cookies:/tmp/gemini_webapi`
- 环境变量从 `.env` 文件读取

### 2. `.env`
存储您的 Gemini cookies（已包含您提供的值）：
- `GEMINI_COOKIE_1PSID`
- `GEMINI_COOKIE_1PSIDTS`

⚠️ **安全提示**：`.env` 文件已添加到 `.gitignore`，不会被提交到 Git

### 3. `gemini_cookies/` 目录
用于持久化存储自动刷新的 cookies，容器重启后无需重新认证

## 使用方法

### 启动服务
```bash
docker-compose up -d
```

### 查看日志
```bash
docker-compose logs -f
```

### 停止服务
```bash
docker-compose down
```

### 重启服务（保留 cookies）
```bash
docker-compose restart
```

## 注意事项

1. **修改启动命令**：请将 `docker-compose.yml` 中的 `python your_app.py` 改为您实际的应用启动命令

2. **端口配置**：默认映射 `8000:8000`，根据需要修改

3. **权限问题**：确保 `gemini_cookies/` 目录有写入权限
   ```bash
   chmod 755 gemini_cookies/
   ```

4. **Cookie 更新**：容器会自动刷新 cookies 并保存到 `gemini_cookies/` 目录

## 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `GEMINI_COOKIE_PATH` | Cookie 存储路径 | `/tmp/gemini_webapi` |
| `GEMINI_COOKIE_1PSID` | Google 认证 cookie | `g.a000...` |
| `GEMINI_COOKIE_1PSIDTS` | Google 认证时间戳 | `sidts-...` |

## 故障排查

### Cookie 未持久化
检查卷映射是否正确：
```bash
docker-compose exec gemini-api ls -la /tmp/gemini_webapi
```

### 权限错误
给予容器写入权限：
```bash
chmod -R 777 gemini_cookies/
```

### Cookie 过期
重新获取 cookies 并更新 `.env` 文件，然后重启：
```bash
docker-compose restart
```
