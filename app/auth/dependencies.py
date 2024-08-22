# app/auth/dependencies.py

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.redis_client import verify_token_and_redis
from app.core.config import settings  # 설정 파일에서 시크릿 키를 가져옴

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 인증 디펜던시: 요청 헤더에서 JWT 토큰을 가져와 검증
async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return None, "토큰이 없습니다."  # 토큰이 없을 경우

    try:
        # JWT 토큰을 디코딩할 때 settings.jwt_secret_key 사용
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not user_id:
            return None, "유효하지 않은 토큰입니다."  # 유저 정보가 없을 경우

        # Redis에서 토큰 유효성 검증
        is_valid = await verify_token_and_redis(token)
        if not is_valid:
            return None, "Redis에서 토큰이 유효하지 않습니다."

        return user_id, None  # 유효한 경우 user_id 반환
    except jwt.ExpiredSignatureError:
        return None, "토큰이 만료되었습니다."  # 만료된 토큰일 경우
    except jwt.InvalidTokenError:
        return None, "유효하지 않은 토큰입니다."  # 유효하지 않은 토큰일 경우
