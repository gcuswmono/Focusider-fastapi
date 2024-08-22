# app/redis_client.py

import redis.asyncio as redis
import json
import jwt
from app.core.config import settings
from fastapi import HTTPException

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


# JWT 토큰 검증 및 Redis에서 확인하는 함수
async def verify_token_and_redis(token: str):
    try:
        # JWT 토큰을 해독
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

        # Redis에서 유효한 토큰인지 확인
        stored_token = await redis_client.get(f"token:{user_id}")
        if not stored_token or stored_token != token:
            raise HTTPException(status_code=401, detail="로그인 후 이용바랍니다.")

        return user_id  # 유저 ID 반환
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="토큰이 만료되었습니다. 다시 로그인해주세요."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
