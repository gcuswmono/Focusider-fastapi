# app/services.py

import json
import random
import openai
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ChatHistory, Article
from app.redis_client import redis_client
from sqlalchemy import text
from config.settings import settings

openai.api_key = settings.openai_api_key

client = openai.OpenAI()


# Redis에서 채팅 상태 가져오기
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
    await redis_client.set(key, json.dumps(state))


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
        return response["choices"][0]["message"]["content"]

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


# 유저가 본 적 없는 랜덤 article을 가져오는 함수
async def get_random_unseen_article(member_id: int, db: AsyncSession):
    # 유저가 이미 본 article의 ID 가져오기
    seen_articles = (
        (
            await db.execute(
                text(
                    "SELECT article_id FROM chat_history WHERE member_id = :member_id"
                ),
                {"member_id": member_id},
            )
        )
        .scalars()
        .all()
    )

    # 이미 본 article을 제외한 랜덤 article 가져오기
    unseen_articles = (
        await db.execute(
            text("SELECT * FROM article WHERE id NOT IN :seen_articles"),
            {"seen_articles": tuple(seen_articles) if seen_articles else (-1,)},
        )
    ).all()  # 전체 Article 객체를 가져옴

    if not unseen_articles:
        raise ValueError("No unseen articles available for this user.")

    # 랜덤으로 하나의 article 선택
    selected_article = random.choice(unseen_articles)

    # 채팅 상태를 Redis에 TTL과 함께 저장
    await set_chat_ttl(member_id, selected_article.id)

    return selected_article


async def handle_chat(
    member_id: int, article_id: int, user_answer: str, db: AsyncSession
):
    try:
        # Redis에서 채팅 상태를 가져옴
        state = await get_chat_state(member_id, article_id)
        print("Chat State:", state)  # 상태 출력
        current_step = state["current_step"]

        chat_history = state.get("chat", [])

        if not chat_history:
            article = await db.get(Article, article_id)
            if not article:
                raise ValueError("Article not found")
            prompt = f"Article: {article.content}\nUser Answer: {user_answer}\nNext Question:"
        elif current_step <= 5:
            prompt = f"Previous Chat: {chat_history}\nUser Answer: {user_answer}\nNext Question:"
        else:
            prompt = f"Summarize the conversation: {state['chat']}"

        # GPT 응답 생성
        gpt_response = await gpt_generate_response(prompt)
        print("GPT Response:", gpt_response)  # GPT 응답 출력

        # 채팅 내역 업데이트
        state["chat"].append({"question": gpt_response, "answer": user_answer})
        state["current_step"] += 1
        await save_chat_state(member_id, article_id, state)

        return gpt_response
    except Exception as e:
        print(f"Error in handle_chat: {str(e)}")
        raise
