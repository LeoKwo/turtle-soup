from pydantic import BaseModel, Field

class Soup(BaseModel):
    """海龟汤汤面标准格式。必须返回此格式的JSON。"""
    # start: str = Field(description="海龟汤汤面起因。一个十分常见的行为或场景。")
    # end: str = Field(description="海龟汤汤面结果。一个令人惊讶、意想不到、摸不着头脑的结果。")
    soup: str = Field(description="海龟汤汤面。一句话描述一个诡异或令人困惑、惊讶但有真实存在可能性的结果。")
    # truth: str = Field(description="故事真相。解释完整故事发生了什么，要求合理但出人意料。")

class Story(BaseModel):
    """悬疑故事标准格式。必须返回此格式的JSON。"""
    story: str = Field(description="悬疑故事。必须合乎逻辑并且烧脑。在此基础上越恐怖邪门越好。")