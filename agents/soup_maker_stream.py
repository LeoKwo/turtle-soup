from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.soup import Soup
from settings import getLLM
import re

# 初始化 Ollama LLM
llm = getLLM(model="qwen3:14b", temperature=0.9)

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Soup)

# Prompt 模板
prompt = PromptTemplate.from_template("""
你是一位擅长创作海龟汤汤面的悬疑作家。汤面包含【起因】和【结果】

请根据以下海龟汤故事创作一个高质量的恐怖悬疑海龟汤汤面：

【海龟汤故事】：
{truth}


请生成以下内容：
【起因】：一句话内话描述这个故事的开头。不要交代剧透内容，只需描述故事开场的画面。如果有人物出场，请给出人物姓名。如有必要，可以包含地点和设定。
【结果】：一句话内话总结这个故事的结尾。不要交代剧透内容！！！

要求：
【起因】与【结果】必须来自提供的海龟汤故事

输出格式：
    {{
        "start": 汤面起因
        "end": 汤面结果
    }}
""")

# 主流程
async def make_soup(truth: str, result_holder: dict[str, Soup | None]):
    chain = prompt | llm
    output_chunks = []

    # LLM开始生成
    # result = chain.invoke(truth)
    
    async for event in chain.astream_events({
        "truth": truth
    }):
        kind = event['event']
        if kind == "on_chat_model_stream":
            content = event['data']["chunk"].content
            output_chunks.append(content)
            yield content 
            
    # Once streaming is done, post-process the output
    full_output = "".join(output_chunks)
    cleaned_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    cleaned_output = re.sub(r"<think\s*/>", "", cleaned_output)

    try:
        result = outputParser.invoke(cleaned_output)
    except Exception as e:
        print("Parsing FAILED:", e)
        result = None

    if isinstance(result, Soup):
        print("parsed correct")
        # return result
    else:
        print("parsed FAILED")
        # return {
        #     "surface": "!!!---PYDANTIC PARSING FAILED---!!!"
        # }
        result = None
    
    # Store the result in the holder
    result_holder["parsed_result"] = result

if __name__ == "__main__":
    make_soup("悬疑", "医生", "医院", "爱情")
