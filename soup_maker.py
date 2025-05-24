from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from formats.soup import Soup
from settings import LLM_MODEL, LLM

# 初始化 Ollama LLM
llm = LLM

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Soup)

# Prompt 模板
prompt_template = PromptTemplate.from_template("""
你是一位擅长创作海龟汤汤面的悬疑作家。汤面包含【起因】和【结果】

请根据以下海龟汤故事创作一个高质量的恐怖悬疑海龟汤汤面：

【海龟汤故事】：
{truth}


请生成以下内容：
【起因】：三句话内话描述这个故事的开头。不要交代太多剧透内容，只需描述故事开场的画面。如果有人物出场，请给出人物姓名。如有必要，可以包含地点和设定。
【结果】：三句话内话总结这个故事的结尾。不要交代剧透内容！！！

要求：
【起因】与【结果】必须来自提供的海龟汤故事

输出格式：
    {{
        "start": 汤面起因
        "end": 汤面结果
    }}
""")
# prompt_template = """
# 你是一位擅长创作海龟汤【汤面】的悬疑作家。

# 请根据以下关键词创作一个高质量的恐怖悬疑海龟汤汤面：

# 风格：{style}
# 角色：{character}
# 场景：{setting}
# 主题：{theme}

# 请生成以下内容：
# 【汤面】：一句话描述一个诡异或令人困惑、惊讶但有真实存在可能性的结果。尽可能的使用意想不到的情节。

# 要求：
# 不考虑故事真相，你的任务仅仅是创作一个足够简洁的海龟汤故事汤面。
# 【汤面】不提供任何背景或解释。应足够简洁和奇怪，最好的汤面应该能让人一眼无法猜出故事的情节。
# 故事必须原创，不得抄袭已知谜题。在满足逻辑闭环成立的前提下，尽可能多的加入恐怖和悬疑元素。

# 输出格式：
#     {{
#         "soup": 汤面
#     }}
# """

# 主流程
def make_soup(truth: str):
    promptNEW = PromptTemplate(
        input_variables=["truth"], template=prompt_template
    )
    chain = promptNEW | llm | outputParser

    # LLM开始生成
    result = chain.invoke(truth)
    # print("\n🧪 生成的海龟汤谜题：")
    # print("=" * 40)
    # print(result)
    # print("=" * 40)

    if isinstance(result, Soup):
        print("parsed correct")
        return result
    else:
        print("parsed FAILED")
        return {
            "surface": "!!!---PYDANTIC PARSING FAILED---!!!"
        }

if __name__ == "__main__":
    make_soup("悬疑", "医生", "医院", "爱情")
