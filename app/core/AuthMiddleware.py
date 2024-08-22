from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
from config import settings

# Redis 클라이언트 생성
redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)

app = FastAPI()


# 인증 미들웨어
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 요청 헤더에서 API 키를 가져옴
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise HTTPException(status_code=401, detail="API Key is missing")

        # Redis에서 API 키 검증
        is_valid = await redis_client.get(api_key)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        # API Key가 유효하면 다음 요청으로 넘김
        response = await call_next(request)
        return response


# 미들웨어 추가
app.add_middleware(AuthMiddleware)
