# main.py

from fastapi import FastAPI, Request
from app.api import chat, article
from app.auth.dependencies import get_current_user  # 인증 함수 가져옴
from app.schemas.common_schemas import ResponseSchema

app = FastAPI()


# 미들웨어에서 전역적으로 인증 처리
@app.middleware("http")
async def verify_login_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        # 토큰이 없을 때의 처리
        return (
            ResponseSchema(
                status=401, message="로그인 후 이용바랍니다.", data=None
            ).model_dump_json(),
            401,
        )

    # 토큰에서 'Bearer '를 제거하고 검증
    token = token[len("Bearer ") :]
    user_id, error_message = await get_current_user(
        token=token
    )  # dependencies에서 검증된 결과 받아옴

    if not user_id:  # 검증 실패 시 처리
        # 구체적인 에러 메시지를 포함해 반환
        return (
            ResponseSchema(
                status=401, message=error_message, data=None
            ).model_dump_json(),
            401,
        )

    # 성공 시 다음 요청 처리
    response = await call_next(request)
    return response


# 도메인별 라우터 설정 (각 API에서 별도 인증 필요 없음)
app.include_router(chat.router, prefix="/fastapi")
app.include_router(article.router, prefix="/fastapi")
