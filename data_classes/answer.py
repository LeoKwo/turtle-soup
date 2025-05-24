from pydantic import BaseModel, Field

class Answer(BaseModel):
    """海龟汤回答标准格式。必须返回此格式的JSON。"""
    answer: str = Field(description="对玩家问题的答复，只能回答 是，否，或者 不相关")
