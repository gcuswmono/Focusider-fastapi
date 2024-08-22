# app/redis_client.py

import redis.asyncio as redis
import json
from app.core.config import settings

# Redis 클라이언트 설정 (decode_responses=True로 UTF-8로 디코딩)
redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)


# Redis에 데이터 저장 (JSON으로 직렬화하여 저장)
async def set_redis_data(key: str, value: dict):
    # 데이터를 JSON으로 직렬화 (ensure_ascii=False로 비ASCII 문자 처리)
    serialized_value = json.dumps(value, ensure_ascii=False)
    await redis_client.setex(key, settings.redis_ttl, serialized_value)


# Redis에서 데이터 가져오기 (JSON으로 역직렬화하여 반환)
async def get_redis_data(key: str):
    data = await redis_client.get(key)
    if data:
        return json.loads(data)  # 데이터를 JSON으로 역직렬화
    return None
