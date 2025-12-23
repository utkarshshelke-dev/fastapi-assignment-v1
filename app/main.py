from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .websocket_manager import manager
from .restaurant_service import get_restaurant_recommendations

app = FastAPI()

@app.websocket("/ws/location")
async def location_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            lat = data.get("latitude")
            lng = data.get("longitude")

            if lat is None or lng is None:
                await manager.send(websocket, {
                    "error": "latitude and longitude required"
                })
                continue

            restaurants = get_restaurant_recommendations(lat, lng)

            await manager.send(websocket, {
                "latitude": lat,
                "longitude": lng,
                "recommendations": restaurants
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
