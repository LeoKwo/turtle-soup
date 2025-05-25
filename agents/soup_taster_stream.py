from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import re
from settings import getLLM
from data_classes.score import Score


temperature=0

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Score)

scoring_prompt = PromptTemplate.from_template("""
    你是一个非常严格的逻辑严密、擅长评估海龟汤谜题质量的悬疑作家兼职评论员。

                                              
    以下是一个海龟汤谜题：
                                              
    【用户输入】：
    风格：{style}
    角色：{character}
    场景：{setting}
    主题：{theme}

    【海龟汤故事】：
    {truth}

    【注意】：海龟汤故事仅仅是汤底的故事真相，并不包括汤面。
    请你从以下四个维度对这个谜题打分（0~10）并进行简短评论：

    1. 迷惑性（是否能引发玩家好奇）1-10：
    2. 逻辑性（故事是否自洽）1-10：
    3. 创意性（是否新颖独特）1-10：
    4. 吸引力（是否能激发提问）1-10：

    输出格式：
    {{
        "confusion": {{"score": integer, "comment": "brief explanation"}},
        "coherence": {{"score": integer, "comment": "brief explanation"}},
        "creativity": {{"score": integer, "comment": "brief explanation"}},
        "engagement": {{"score": integer, "comment": "brief explanation"}}
    }}
""")

async def taste_soup(style: str, character: str, setting: str, theme: str, truth: str, result_holder: dict[str, Score | None]):
    llm = getLLM(temperature=temperature)
    
    scoring_chain = scoring_prompt | llm
    output_chunks = []

    async for event in scoring_chain.astream_events({
        "truth": truth,
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme
    }):
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

    if isinstance(result, Score):
        print("\nparsed correct\n")
    else:
        print("\nparsed FAILED\n")
        result = None

    # Store the result in the holder
    result_holder["parsed_result"] = result

