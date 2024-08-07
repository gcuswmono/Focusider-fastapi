### README.md (English Version)

# FastAPI GPT-4o-mini Chat API

This project is a FastAPI application that interfaces with the OpenAI GPT-4o-mini model to create a chat service. The chat service supports conversation initiation and termination flags.

## Project Structure

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

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Httpx
- Pydantic
- Python-dotenv

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/my_fastapi_project.git
    cd my_fastapi_project
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**
    Create a `.env` file in the project root and add your OpenAI API key:
    ```plaintext
    GPT_API_KEY=your_openai_api_key
    GPT_API_BASE_URL=https://api.openai.com/v1
    ```

5. **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

### Endpoint: `/api/chat`

**Method:** POST

**Request:**
```json
{
    "messages": [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help you?"}
    ],
    "start_conversation": true
}
```

**Response:**
```json
{
    "reply": "Hello! How can I assist you today?"
}
```

## License

This project is licensed under the MIT License.