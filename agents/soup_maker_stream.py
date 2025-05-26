from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.soup import Soup
from settings import getLLM
import re

# 初始化 Ollama LLM
temperature=0.9

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Soup)

# Prompt 模板
prompt = PromptTemplate.from_template("""
你是一个海龟汤谜题设计师，请直接根据提供的汤底故事创作一个令人毛骨悚然的汤面谜题。

【海龟汤故事】
{truth}
                                      
【要求】
1. 用1句话制造离奇场景（包含时间+地点+异常现象）
2. 植入表面矛盾的细节
3. 最后用问句点出核心矛盾
                                      
【输出示例】
"凌晨三点，停尸房的尸体全部面朝墙壁站立，监控显示整夜无人进入。为什么尸检报告显示死者生前最后看到的是星空？"

【格式要求】
{{
    "soup": "你的汤面谜题"
}}
""")

# 主流程
async def make_soup(truth: str, result_holder: dict[str, Soup | None]):
    llm = getLLM(temperature=temperature)

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
