import json
from fastapi import HTTPException
import openai
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_history import ChatHistory
from app.models.article import Article
from app.redis_client import get_redis_data, redis_client
from app.core.config import settings

openai.api_key = settings.openai_api_key

client = openai.OpenAI()


async def get_chat_state(member_id: int, article_id: int):
    key = f"chat:{member_id}:{article_id}"
    state = await redis_client.get(key)
    print(f"Redis에서 불러온 데이터 (Key: {key}): {state}")  # 불러온 데이터 출력
    if state:
        return json.loads(state)  # JSON 형식으로 파싱
    return {"current_step": 1, "chat": []}  # 저장된 상태가 없으면 기본값 반환


# Redis에 채팅 상태 저장
async def save_chat_state(member_id: int, article_id: int, state: dict):
    key = f"chat:{member_id}:{article_id}"
    await redis_client.set(key, json.dumps(state, ensure_ascii=False))


# GPT-4o-mini 모델을 호출하는 함수
def gpt_generate_response(user_question: str):
    try:
        # GPT-4o-mini 모델에 메시지 전달
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # GPT-4o-mini 모델 사용
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },  # 시스템 메시지
                {"role": "user", "content": user_question},  # 동적으로 전달된 유저 질문
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        # GPT 응답 출력
        return response.choices[0].message.content

    except openai.APIConnectionError as e:
        print(f"OpenAI API Error: {e}")
        return None


async def set_chat_ttl(member_id: int, article_id: int, ttl: int = 3600):
    key = f"chat:{member_id}:{article_id}"
    # 초기 상태를 설정 (채팅 단계와 빈 채팅 내역)
    chat_state = {"current_step": 1, "chat": []}
    # Redis에 JSON 형식으로 저장 (TTL 적용)
    await redis_client.set(key, json.dumps(chat_state), ex=ttl)
    print(f"Redis에 저장된 Key: {key}, 데이터: {chat_state}, TTL: {ttl}")


async def handle_chat(
    member_id: int, article_id: int, user_answer: str, db: AsyncSession
):
    try:
        # Redis에서 채팅 상태를 가져옴
        state = await get_chat_state(member_id, article_id)
        print("Chat State:", state)  # 상태 출력
        current_step = state["current_step"]
        redisstate = await get_redis_data(f"chat:{member_id}:{article_id}")
        print("Redis State:", redisstate)

        chat_history = state.get("chat", [])

        if not chat_history:
            article = await db.get(Article, article_id)
            if not article:
                raise ValueError("Article not found")
            prompt = f"answer in in korean. Article: {article.content}\nUser Answer: {user_answer}\nNext Question:"
        elif current_step < 5:
            prompt = f"answer in in korean. Previous Chat: {chat_history}\nUser Answer: {user_answer}\nNext Question:"
        else:
            prompt = f"Summarize the conversation: {state['chat']}"
            # GPT 응답 생성
            gpt_response = gpt_generate_response(prompt)
            print("GPT Summary Response:", gpt_response)

            # 최종 대화 내용을 MariaDB에 저장
            new_chat_history = ChatHistory(
                member_id=member_id,
                chat=json.dumps(state["chat"]),  # 대화 내역을 JSON으로 저장
                article_id=article_id,
            )
            db.add(new_chat_history)
            await db.commit()  # DB에 저장 및 커밋
            print("Chat history saved to DB.")

            # Redis에서 해당 데이터를 삭제
            await redis_client.delete(f"chat:{member_id}:{article_id}")
            print(f"Deleted Redis key: chat:{member_id}:{article_id}")

            return gpt_response

        # GPT 응답 생성
        gpt_response = gpt_generate_response(prompt)
        print("GPT Response:", gpt_response)  # GPT 응답 출력

        # 채팅 내역 업데이트
        state["chat"].append({"question": gpt_response, "answer": user_answer})
        state["current_step"] += 1
        await save_chat_state(member_id, article_id, state)

        return gpt_response
    except ValueError as e:
        print(f"Error in handle_chat: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in handle_chat: {str(e)}")
        raise
