import asyncio
from app.models import Base
from app.database import engine

# 비동기 DB 초기화 함수
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 이벤트 루프를 명시적으로 관리
def run_async_task():
    loop = asyncio.new_event_loop()  # 새로운 이벤트 루프 생성
    asyncio.set_event_loop(loop)     # 이벤트 루프 설정
    
    try:
        loop.run_until_complete(init_db())  # 비동기 작업 실행
    finally:
        # 비동기적으로 dispose를 호출
        loop.run_until_complete(engine.dispose())
        loop.close()  # 작업이 끝나면 이벤트 루프 종료

if __name__ == "__main__":
    run_async_task()
