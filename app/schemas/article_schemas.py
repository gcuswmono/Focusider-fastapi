from pydantic import BaseModel


# 기사 관련 응답 데이터 스키마
class ArticleResponseData(BaseModel):
    contents: str  # 기사 내용
    question: str  # 기사에 대한 질문
    article_id: int  # 기사 ID


# 멤버 요청 데이터를 검증하는 스키마
class MemberRequestSchema(BaseModel):
    member_id: int  # 유저의 ID
