from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.reflection import Reflection
from data_classes.score import Score
from settings import getLLM
import re

# 初始化模型
model="qwen3:14b"
temperature=0

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Reflection)

reflect_prompt = PromptTemplate.from_template("""
    你是一位擅长反思的悬疑作家，专长是评论“海龟汤”类的谜题故事。

    【用户输入】：
    风格：{style}
    角色：{character}
    场景：{setting}
    主题：{theme}
    
    以下是上一轮生成的故事及其评分反馈：
    【海龟汤故事】：{truth}

    【评分】：
    {score}

    请根据这些反馈，思考可以改进的地方。  
    用一句话总结这个故事的主要缺点，并给出一个明确可执行的策略，用于改进下一轮生成的故事。

    请用以下 JSON 格式回复：
    {{
        "weakness": "一句话总结主要的缺点",
        "strategy": "用于改进下一轮的可执行的简短策略"
    }}
""")

async def analyze_soup(
        style: str, 
        character: str, 
        setting: str, 
        theme: str, 
        truth: str, 
        score: Score,
        result_holder: dict[str, Reflection | None]
    ):

    llm = getLLM(model=model, temperature=temperature)
    
    reflect_chain = reflect_prompt | llm
    output_chunks = []
    
    async for event in reflect_chain.astream_events({
        "truth": truth,
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme,
        "score": score
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


    if isinstance(result, Reflection):
        print("parsed correct")
    else:
        print("parsed FAILED")
        result = None
    
    # Store the result in the holder
    result_holder["parsed_result"] = result
