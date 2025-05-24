from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.reflection import Reflection
from data_classes.score import Score
from settings import LLM_MODEL, LLM

# 初始化模型
llm = LLM

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

def analyze_soup(
        style: str, 
        character: str, 
        setting: str, 
        theme: str, 
        truth: str, 
        score: Score
    ):
    
    reflect_chain = reflect_prompt | llm | outputParser

    result = reflect_chain.invoke({
        "truth": truth,
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme,
        "score": score
    })
    # print("\n海龟汤故事反思结果：")
    # print("=" * 40)
    # print(result)
    # print("=" * 40)

    if isinstance(result, Reflection):
        print("parsed correct")
        return result
    else:
        print("parsed FAILED")
        return {
            "score": "!!!---PYDANTIC PARSING FAILED---!!!"
        }