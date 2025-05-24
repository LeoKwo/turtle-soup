from pydantic import BaseModel, Field

class Scoring(BaseModel):
    score: int = Field(description="单项评分。")
    comment: str = Field(description="单项评论。简单描述你发现的问题。")

class Score(BaseModel):
    """海龟汤评分标准格式。必须返回此格式的JSON。"""
    confusion: Scoring = Field(description="迷惑性（是否能引发玩家好奇）")
    coherence: Scoring = Field(description="逻辑性（故事是否自洽）")
    creativity: Scoring = Field(description="创意性（是否新颖独特）")
    engagement: Scoring = Field(description="吸引力（是否能激发提问）")