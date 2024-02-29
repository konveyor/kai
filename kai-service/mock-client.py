# Mock a client doing client things
import aiohttp
import asyncio


async def main():
  async with aiohttp.ClientSession('http://0.0.0.0:8080') as session:
    async with session.post('/dummy_json_request', json={"test": "object"}):
      print('yo')


asyncio.run(main())