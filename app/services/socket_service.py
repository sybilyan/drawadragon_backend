from fastapi import WebSocket

from app.services.sd_service import generate_image_by_lcm


async def handle_websocket_client(client: WebSocket):
    while True:
        print("[INFO] waiting for client data...")

        data = await client.receive_json()
        result = generate_image_by_lcm(data)

        if result != None:
            await client.send_text(result)
