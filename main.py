from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.post("/alert")
async def receive_alert(request: Request):
    data = await request.json()

    if isinstance(data.get("content"), dict):
        content_string = ", ".join(f"{k}: {v}" for k, v in data["content"].items())
        payload = {"content": content_string}
    else:
        payload = data

    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK_URL, json=payload)

    return {"status": "ok"}
