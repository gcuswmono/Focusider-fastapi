# app/redis_client.py

import redis.asyncio as redis
from config.settings import settings

redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)


async def set_redis_data(key: str, value: str):
    await redis_client.setex(key, settings.redis_ttl, value)


async def get_redis_data(key: str):
    return await redis_client.get(key)
