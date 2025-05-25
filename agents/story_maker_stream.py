from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.soup import Story
from data_classes.reflection import Reflection
from data_classes.score import Score
from typing import Any
from settings import getLLM
import re

# 初始化 Ollama LLM
temperature=0.9

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
你是一位擅长创作海龟汤故事的推理悬疑作家，请直接构建符合以下要求的完整汤底：

1. 模式选择（二选一）：
    - 现实模式：基于[科学原理/职业知识/社会常识]构建核心诡计
    - 幻想模式：声明[超自然法则]+[现实映射规则]双系统

2. 基础元件：
    - 必须包含1个「常识折叠点」（如将次声波共振伪装成鬼哭）
    - 必须设计2个「悖论线索」（用※标记红鲱鱼）

3. 逻辑验证：
    - 现实模式：通过[奥卡姆剃刀测试]（最简单解释覆盖所有线索）
    - 幻想模式：通过[法则兼容性测试]（不违反自设世界观）

4. 从以下套路中选择一个：
    {tropes}

5. 禁止项：
    - 现实模式不得出现超自然解释
    - 幻想模式不得有未声明的隐藏法则

在满足以上条件时，按照以下用户自定义的参数生成符合要求的海龟汤：
【用户自定义海龟汤故事参数】
风格：{style}
角色：{character}
场景：{setting}
主题：{theme}

请给出完整的海龟汤汤底故事 **400字以内**，不需要考虑海龟汤汤面：

输出格式：
    {{
        "story": 悬疑故事
    }}
"""

# 主流程
async def make_story(
        style: str, 
        character: str, 
        setting: str, 
        theme: str, 
        result_holder: dict[str, Score | None], 
        tropes: list[dict[str, Any]] = default_tropes
    ):
    llm = getLLM(temperature=temperature)

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
    output_chunks = []
    chain = prompt | llm

    async for event in chain.astream_events(input):
        kind = event['event']
        if kind == "on_chat_model_stream":
            content = event['data']["chunk"].content
            # print(content, end="", flush=True)
            output_chunks.append(content)
            yield content  # stream each chunk to st.write_stream

    # Once streaming is done, post-process the output
    full_output = "".join(output_chunks)
    cleaned_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    cleaned_output = re.sub(r"<think\s*/>", "", cleaned_output)

    try:
        result = outputParser.invoke(cleaned_output)
    except Exception as e:
        print("Parsing FAILED:", e)
        result = None

    if isinstance(result, Story):
        print("parsed correct")
    else:
        print("parsed FAILED")
        result = None

    # Store the result in the holder
    result_holder["parsed_result"] = result
    
# 测试
if __name__ == "__main__":
    make_story(
        style="超自然",
        character="村民",
        setting="月圆之夜",
        theme="猎奇"
    )
