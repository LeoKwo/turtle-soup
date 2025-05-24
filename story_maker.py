from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.soup import Story
from data_classes.reflection import Reflection
from data_classes.score import Score
from typing import Any
from settings import LLM_MODEL, LLM

# 初始化 Ollama LLM
llm = LLM

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Story)

# 套路
default_tropes = [
    {
        "id": "reversal",
        "name": "反转型",
        "description": "结局出人意料，往往表面看似合理甚至幸福，实则隐藏着悲剧或讽刺。",
        "keywords": ["出人意料", "真相反转", "讽刺", "悲剧"]
    },
    {
        "id": "misunderstanding",
        "name": "信息差型",
        "description": "主角因为信息缺失或误解而做出看似不合理的行为，玩家需还原完整背景。",
        "keywords": ["误解", "隐藏信息", "误会", "信息不对称"]
    },
    {
        "id": "death",
        "name": "死亡型",
        "description": "涉及离奇的死亡、自杀或谋杀事件，真相通常令人震惊或难以置信。",
        "keywords": ["自杀", "他杀", "谋杀", "事故", "尸体"]
    },
    {
        "id": "fragment",
        "name": "片段型",
        "description": "只呈现故事的某个片段或结尾，引导玩家还原时间线和完整事件。",
        "keywords": ["结局先行", "镜头切换", "时间跳跃"]
    },
    {
        "id": "identity",
        "name": "身份错位型",
        "description": "故事中角色身份存在误导或反转，真相依赖对身份认知的纠正。",
        "keywords": ["角色反转", "冒充", "替身", "盲点"]
    },
    {
        "id": "unreality",
        "name": "幻想/非现实型",
        "description": "事件发生在梦境、影视、幻想或精神异常场景中，与现实脱节。",
        "keywords": ["幻想", "梦境", "虚拟现实", "精神病", "非真实"]
    },
    {
        "id": "moral",
        "name": "道德抉择型",
        "description": "主角面临伦理困境或两难选择，事件涉及牺牲、救赎或价值观冲突。",
        "keywords": ["伦理", "牺牲", "道德", "人性", "灰色地带"]
    }
]


# Prompt 模板
prompt_template_new = """
你是一位擅长创作悬疑故事的悬疑作家。

请根据以下以下的故事信息，使用逻辑和你的悬疑写作方法创作一个悬疑故事：

风格：{style}
角色：{character}
场景：{setting}
主题：{theme}

请生成以下内容：
【故事】：一篇基于上述信息创作的悬疑故事。必须合乎逻辑并且烧脑。

要求：
故事必须符合逻辑。结局必须非常出人意料但在情理之中。**400字以内**
【故事】必须原创，不得抄袭已知谜题。
包括以下内容：1. 离奇结尾描述（供玩家推理）；2. 完整故事真相；题目应符合下列套路类型之一：
{tropes}

输出格式：
    {{
        "story": 悬疑故事
    }}
"""

prompt_template_remake = """
    你是一位擅长编辑悬疑故事的悬疑小说编辑。

    请根据以下以下的信息，使用逻辑和悬疑风格修改以下的悬疑故事：

    风格: {style}
    角色: {character}
    场景: {setting}
    主题: {theme}
    故事真相: {truth}
    故事评分: {score}
    改进建议: {reflection}

    请生成以下内容：
    【故事】：一篇基于上述信息创作的悬疑故事。必须合乎逻辑并且烧脑。

    要求：
    故事必须符合逻辑。结局必须非常出人意料但在情理之中。**400字以内**
    【故事】必须原创，不得抄袭已知谜题。
    包括以下内容：1. 离奇结尾描述（供玩家推理）；2. 完整故事真相；题目应符合下列套路类型之一：
    {tropes}

    输出格式：
        {{
            "story": 修改后的悬疑故事
        }}
"""

# 主流程
def make_story(style: str, character: str, setting: str, theme: str, tropes: list[dict[str, Any]] = default_tropes):
    input = {
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme,
        "tropes": tropes
    }
    prompt = PromptTemplate(
        input_variables=[input.keys()], template=prompt_template_new
    )
    chain = prompt | llm | outputParser

    # LLM开始生成
    result = chain.invoke(input)
    # print("\n🧪 生成的海龟汤故事真相：")
    # print("=" * 40)
    # print(result)
    # print("=" * 40)

    if isinstance(result, Story):
        print("parsed correct")
        return result
    else:
        print("parsed FAILED")
        return {
            "truth": "!!!---PYDANTIC PARSING FAILED---!!!"
        }
    
# 后续流程
def remake_story(style: str, character: str, setting: str, theme: str, truth: str, score: Score, reflection: Reflection, tropes: list[dict[str, Any]] = default_tropes):
    input = {
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme,
        "tropes": tropes,
        "truth": truth,
        "score": score,
        "reflection": reflection
    }
    prompt = PromptTemplate(
        input_variables=[input.keys()], template=prompt_template_remake
    )
    chain = prompt | llm | outputParser

    # LLM开始生成
    result = chain.invoke(input)
    # print("\n🧪 改进的海龟汤故事真相：")
    # print("=" * 40)
    # print(result)
    # print("=" * 40)

    if isinstance(result, Story):
        print("parsed correct")
        return result
    else:
        print("parsed FAILED")
        return {
            "truth": "!!!---PYDANTIC PARSING FAILED---!!!"
        }

# 测试
if __name__ == "__main__":
    make_story(
        style="超自然",
        character="村民",
        setting="月圆之夜",
        theme="猎奇"
    )
