import asyncio
from notifications import send_notifications


async def scheduler(bot):

    while True:

        await send_notifications(bot)

        await asyncio.sleep(86400)