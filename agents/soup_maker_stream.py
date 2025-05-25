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
你是一个专业的海龟汤谜题（汤面）设计师。

请根据以下海龟汤故事创作一个高质量的恐怖悬疑海龟汤汤面：
【海龟汤故事】：
{truth}

请生成以下内容：
故事谜面：
1. 开场冲击：用[时间/地点/人物状态]制造反常识场景（如'凌晨三点，男人笑着看妻子切洋葱，突然报警'）
2. 细节迷雾：植入3个表面矛盾的细节（如'现场有打翻的水杯但无指纹''死者手握未拆封的救生衣'）
3. 悬念锚点：在结尾用问句锁定核心矛盾（如'为什么目击者听到枪声却说不是凶器？'）
4. 信息遮蔽：隐藏1个物理常识或社会常识（如光学折射原理、特定职业工作流程）
                                      
【技术参数】
- 语言简洁度：控制在150字内
- 干扰项密度：每20字埋设1个干扰线索
- 认知偏差类型：必须包含[基本归因错误]+[错误关联暗示]

【输出示例】
（经典结构参考）
午夜医院，护士发现植物人患者死亡时面带微笑，病房窗户大开但积雪平整。为什么尸检显示死因是溺亡？

【输出格式】
    {{
        "soup": 根据故事生成的海龟汤汤面
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
