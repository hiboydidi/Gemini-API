import asyncio
import os
from gemini_webapi import GeminiClient
from aiohttp import web

# 从环境变量获取 cookies
Secure_1PSID = os.getenv("GEMINI_COOKIE_1PSID")
Secure_1PSIDTS = os.getenv("GEMINI_COOKIE_1PSIDTS")

client = None

async def init_client():
    global client
    if not Secure_1PSID or not Secure_1PSIDTS:
        raise ValueError("Missing GEMINI_COOKIE_1PSID or GEMINI_COOKIE_1PSIDTS environment variables")
    
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS)
    await client.init(timeout=30, auto_close=False, auto_refresh=True)
    print("Gemini client initialized successfully")

async def health_check(request):
    return web.json_response({"status": "ok", "message": "Gemini API is running"})

async def generate(request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "")
        
        if not prompt:
            return web.json_response({"error": "Missing prompt"}, status=400)
        
        response = await client.generate_content(prompt)
        
        return web.json_response({
            "text": response.text,
            "images": [{"url": img.url, "title": img.title} for img in response.images] if response.images else []
        })
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def chat(request):
    try:
        data = await request.json()
        messages = data.get("messages", [])
        
        if not messages:
            return web.json_response({"error": "Missing messages"}, status=400)
        
        chat_session = client.start_chat()
        
        responses = []
        for msg in messages:
            response = await chat_session.send_message(msg)
            responses.append(response.text)
        
        return web.json_response({
            "responses": responses,
            "last_response": responses[-1] if responses else ""
        })
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def on_startup(app):
    await init_client()

async def on_cleanup(app):
    if client:
        await client.close()

def create_app():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    app.router.add_post("/generate", generate)
    app.router.add_post("/chat", chat)
    
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8000)
