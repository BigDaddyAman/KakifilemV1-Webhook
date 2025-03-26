import os
import json
import aiohttp
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_PATH = f"/webhook/{os.getenv('BOT_TOKEN')}"
LOCAL_BOT_HOST = os.getenv('LOCAL_BOT_HOST', '127.0.0.1')
LOCAL_BOT_PORT = int(os.getenv('LOCAL_BOT_PORT', 3001))

async def forward_to_local_bot(data):
    """Forward the update to locally running bot"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f'http://{LOCAL_BOT_HOST}:{LOCAL_BOT_PORT}/process_update',
                json=data
            ) as resp:
                return await resp.text()
        except Exception as e:
            print(f"Error forwarding to local bot: {e}")
            return None

async def handle_webhook(request):
    if request.match_info.get('token') != os.getenv('BOT_TOKEN'):
        return web.Response(status=403)

    data = await request.json()
    await forward_to_local_bot(data)
    return web.Response(status=200)

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)

if __name__ == '__main__':
    web.run_app(
        app,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8443))
    )
