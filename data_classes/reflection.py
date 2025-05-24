from pydantic import BaseModel, Field

class Reflection(BaseModel):
    """海龟汤反思标准格式。必须返回此格式的JSON。"""
    weakness: str = Field(description="五句话以内总结主要的缺点")
    strategy: str = Field(description="用于改进下一轮的可执行的简短策略")
