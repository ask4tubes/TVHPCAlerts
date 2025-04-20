from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# Retrieve the Discord Webhook URL from environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.post("/alert")
async def receive_alert(request: Request):
    try:
        # Parse the incoming JSON request
        data = await request.json()

        # Extract the content dictionary
        content = data.get("content", {})

        # Format the message for better readability in Discord
        formatted_message = (
            f"**Symbol:** {content.get('symbol', 'N/A')}\n"
            f"**Pattern:** {content.get('pattern', 'N/A')}\n"
            f"**Direction:** {content.get('direction', 'N/A')}\n"
            f"**Confirmed:** {content.get('confirmed', 'N/A')}\n"
            f"**Timestamp:** {content.get('timestamp', 'N/A')}\n"
            f"**Hop:** {content.get('hop', 'N/A')}\n"
            f"**T1 (Target 1):** {content.get('t1', 'N/A')}\n"
            f"**T2 (Target 2):** {content.get('t2', 'N/A')}\n"
            f"**Terminal:** {content.get('terminal', 'N/A')}\n"
            f"**AB=CD:** {content.get('ab=cd', 'N/A')}\n"
            f"**XA:** {content.get('xa', 'N/A')}\n"
            f"**BC:** {content.get('bc', 'N/A')}\n"
        )

        # Prepare the payload to send to Discord
        payload = {"content": formatted_message}

        # Send the message to Discord
        async with httpx.AsyncClient() as client:
            response = await client.post(DISCORD_WEBHOOK_URL, json=payload)

        # Check if the request was successful
        response.raise_for_status()

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
