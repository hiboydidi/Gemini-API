# Gemini WebAPI HTTP 服务使用指南

这是一个基于 `gemini-webapi` 库构建的 HTTP API 服务。

## 部署后的 API 端点

### 1. 健康检查

**GET** `/` 或 `/health`

检查服务是否正常运行。

**响应示例：**
```json
{
  "status": "ok",
  "message": "Gemini API is running"
}
```

### 2. 生成内容（单次对话）

**POST** `/generate`

发送单次提示词，获取 Gemini 的响应。

**请求体：**
```json
{
  "prompt": "你好，请介绍一下自己"
}
```

**响应示例：**
```json
{
  "text": "你好！我是 Gemini，一个由 Google 开发的大型语言模型...",
  "images": []
}
```

**带图片的响应示例：**
```json
{
  "text": "这是一些猫的图片",
  "images": [
    {
      "url": "https://example.com/cat1.jpg",
      "title": "可爱的猫咪"
    }
  ]
}
```

### 3. 多轮对话

**POST** `/chat`

发送多轮对话消息，保持上下文。

**请求体：**
```json
{
  "messages": [
    "你好",
    "我刚才说了什么？"
  ]
}
```

**响应示例：**
```json
{
  "responses": [
    "你好！很高兴见到你。",
    "你刚才说了"你好"。"
  ],
  "last_response": "你刚才说了"你好"。"
}
```

## 使用示例

### cURL

```bash
# 健康检查
curl https://gemini-api-1tbpvg.fly.dev/health

# 生成内容
curl -X POST https://gemini-api-1tbpvg.fly.dev/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "什么是人工智能？"}'

# 多轮对话
curl -X POST https://gemini-api-1tbpvg.fly.dev/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": ["你好", "今天天气怎么样？"]}'
```

### Python

```python
import requests

# 生成内容
response = requests.post(
    "https://gemini-api-1tbpvg.fly.dev/generate",
    json={"prompt": "写一首关于春天的诗"}
)
print(response.json()["text"])

# 多轮对话
response = requests.post(
    "https://gemini-api-1tbpvg.fly.dev/chat",
    json={"messages": ["你好", "你能做什么？"]}
)
print(response.json()["last_response"])
```

### JavaScript (Fetch)

```javascript
// 生成内容
fetch('https://gemini-api-1tbpvg.fly.dev/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: '解释一下量子计算'
  })
})
.then(res => res.json())
.then(data => console.log(data.text));

// 多轮对话
fetch('https://gemini-api-1tbpvg.fly.dev/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    messages: ['你好', '你会什么语言？']
  })
})
.then(res => res.json())
.then(data => console.log(data.last_response));
```

## 错误处理

API 会返回标准的 HTTP 状态码：

- `200` - 成功
- `400` - 请求参数错误
- `500` - 服务器内部错误

**错误响应示例：**
```json
{
  "error": "Missing prompt"
}
```

## 环境变量

服务需要以下环境变量（已在 Fly.io Secrets 中配置）：

- `GEMINI_COOKIE_1PSID` - Google 认证 cookie
- `GEMINI_COOKIE_1PSIDTS` - Google 认证时间戳
- `GEMINI_COOKIE_PATH` - Cookie 持久化路径（默认：`/data/gemini_webapi`）

## 注意事项

1. **速率限制**：请合理使用 API，避免频繁请求
2. **Cookie 刷新**：服务会自动刷新 cookies，无需手动维护
3. **持久化**：使用 Fly.io 卷挂载确保 cookies 在重启后保留
4. **安全性**：不要将 cookies 暴露在公开代码中

## 本地测试

```bash
# 设置环境变量
export GEMINI_COOKIE_1PSID="your_cookie_here"
export GEMINI_COOKIE_1PSIDTS="your_cookie_ts_here"

# 运行服务
python app.py

# 测试
curl http://localhost:8000/health
```

## Docker 运行

```bash
docker build -t gemini-api .
docker run -p 8000:8000 \
  -e GEMINI_COOKIE_1PSID="your_cookie" \
  -e GEMINI_COOKIE_1PSIDTS="your_cookie_ts" \
  gemini-api
```
