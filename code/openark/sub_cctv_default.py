import asyncio
from pprint import pprint as print
from dotenv import load_dotenv
from openark import OpenArk

load_dotenv()

async def loop_subscribe(ark: OpenArk, model: str) -> None:
    mc = await ark.get_model_channel(model)
    async for data in mc:
        print(data)


if __name__ == '__main__':
    ark = OpenArk()
    asyncio.run(loop_subscribe(ark, 'cctv.default'))