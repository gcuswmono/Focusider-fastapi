### README.md (Korean Version)

# FastAPI GPT-4o-mini 채팅 API

이 프로젝트는 OpenAI GPT-4o-mini 모델과 연동하여 채팅 서비스를 제공하는 FastAPI 애플리케이션입니다. 이 채팅 서비스는 대화의 시작 및 종료 플래그를 지원합니다.

## 프로젝트 구조

```
my_fastapi_project/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── chat.py
│   ├── services/
│   │   ├── gpt_service.py
├── .env
├── .gitignore
├── requirements.txt
```

## 요구 사항

- Python 3.7+
- FastAPI
- Uvicorn
- Httpx
- Pydantic
- Python-dotenv

## 설정

1. **레포지토리 클론:**
    ```bash
    git clone https://github.com/yourusername/my_fastapi_project.git
    cd my_fastapi_project
    ```

2. **가상환경 생성:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4. **환경 변수 설정:**
    프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API 키를 추가합니다:
    ```plaintext
    GPT_API_KEY=your_openai_api_key
    GPT_API_BASE_URL=https://api.openai.com/v1
    ```

5. **애플리케이션 실행:**
    ```bash
    uvicorn app.main:app --reload
    ```

## 사용법

### 엔드포인트: `/api/chat`

**메서드:** POST

**요청:**
```json
{
    "messages": [
        {"role": "user", "content": "안녕하세요!"},
        {"role": "assistant", "content": "안녕하세요! 어떻게 도와드릴까요?"}
    ],
    "start_conversation": true
}
```

**응답:**
```json
{
    "reply": "안녕하세요! 무엇을 도와드릴까요?"
}
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.