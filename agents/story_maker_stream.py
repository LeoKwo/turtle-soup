from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.soup import Story
from data_classes.score import Score
from typing import Any
from settings import getLLM
import re
from few_shot.retriever import search_soup

# 初始化 Ollama LLM
temperature=0.9

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Story)

# 套路
default_tropes = [
    {
        "id": "identity_reversal",
        "name": "身份反转型",
        "description": "角色真实身份与表象完全相反，通过身份错位制造核心诡计。",
        "keywords": ["假死者", "活人伪装", "物种伪装", "双胞胎"]
    },
    {
        "id": "death_puzzle",
        "name": "死亡谜局型",
        "description": "通过非常规死亡方式设计谜题，包含自杀伪装/意外致死/集体死亡等模式。",
        "keywords": ["延时装置", "日常物品致死", "气体泄漏", "心理暗示"]
    },
    {
        "id": "info_trick",
        "name": "信息诡计型",
        "description": "利用叙述性诡计或常识盲区制造认知偏差，包含性别/物种/数量误导。",
        "keywords": ["叙述性诡计", "物理原理", "生物特性", "化学现象"]
    },
    {
        "id": "time_space",
        "name": "时空操作型",
        "description": "通过时间循环、空间错位或维度折叠构建非常规事件逻辑。",
        "keywords": ["记忆错位", "镜像密室", "季节伪装", "微观空间"]
    },
    {
        "id": "psychology",
        "name": "心理暗示型",
        "description": "利用群体认知偏差和红鲱鱼陷阱引导错误推理方向。",
        "keywords": ["从众效应", "语言双关", "刻板印象", "无效线索"]
    },
    {
        "id": "special_rules",
        "name": "特殊设定型",
        "description": "声明超自然规则后在其框架内设计符合逻辑的非常规解答。",
        "keywords": ["拟人法则", "能量守恒", "规则嵌套", "限制条件"]
    }
]


# Prompt 模板
prompt_template_new = """
你是一个专业的海龟汤故事创作助手。请根据以下要素创作一个完整的汤底故事：

【基本要素】
风格：{style}
角色：{character}
场景：{setting}
主题：{theme}

【核心要求】
1. 必须包含一个令人震惊的反转结局
2. 包含2个看似矛盾的线索（用※标记）
3. 解答必须符合以下条件之一：
   - 现实模式：基于科学原理/专业知识/社会常识
   - 幻想模式：有明确声明的超自然规则

【创作步骤】
1. 先确定核心诡计
2. 设计至少两个表面矛盾的线索
3. 构建符合逻辑的解答路径

【禁止事项】
- 不得出现未声明的超自然元素（幻想模式除外）
- 不得使用梦境/精神病等偷懒解释

【参考示例】
可以参考故事情节或者提取其中的套路
{few_shot_examples}

作为参考，可以从以下套路中选择一个：
{tropes}

必须按照以下JSON格式输出完整的海龟汤汤底故事 **150字以内**：

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
        few_shot_examples: str,
        result_holder: dict[str, Score | None], 
        tropes: list[dict[str, Any]] = default_tropes
    ):
    llm = getLLM(temperature=temperature)

    input = {
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme,
        "few_shot_examples": few_shot_examples,
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
