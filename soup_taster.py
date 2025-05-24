from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import json
import re
from formats.score import Score
from settings import LLM_MODEL, LLM

# 初始化 Ollama LLM
llm = LLM

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Score)

scoring_prompt = PromptTemplate.from_template("""
    你是一个逻辑严密、擅长评估海龟汤谜题质量的悬疑作家兼职评论员。

    以下是一个海龟汤谜题：
                                              
    【用户输入】：
    风格：{style}
    角色：{character}
    场景：{setting}
    主题：{theme}

    【海龟汤故事】：
    {truth}

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

def taste_soup(style: str, character: str, setting: str, theme: str, truth: str):
    
    scoring_chain = scoring_prompt | llm | outputParser

    result = scoring_chain.invoke({
        "truth": truth,
        "style": style,
        "character": character,
        "setting": setting,
        "theme": theme
    })
    # print("\n海龟汤谜题评分结果：")
    # print("=" * 40)
    # print(result)
    # print("=" * 40)

    if isinstance(result, Score):
        print("parsed correct")
        return result
    else:
        print("parsed FAILED")
        return {
            "score": "!!!---PYDANTIC PARSING FAILED---!!!"
        }
    

# Example call
if __name__ == "__main__":
    style="超自然"
    character="村民"
    setting="月圆之夜"
    theme="猎奇"
    truth = "月圆之夜，村民们都在熟睡中，李明却独自一人站在村头的老槐树下等朋友。这棵老槐树是村里最古老的树木之一，据说已经活了超过一百年，夜晚时它那淡淡的影子总是伴随着满月的光芒显得格外神秘。\n\n就在这棵树的旁边，有一个小洞穴，里面藏有村民们世代相传的一个秘密：每当月圆之夜，村里的长者便会进入这个小洞穴，向里面的古老神灵祈求安宁与丰收。李明的好友恰好是一位对这些传说充满好奇的年轻人，他打算在这一晚通过神秘的仪式召唤出老槐树中的精灵。\n\n然而，就在李明好友准备进行仪式的时候，一道奇异的光芒突然从地下冒出，紧接着，一股强大的力量将整棵树和周围的一切瞬间拉进了另一个维度。第二天早上，村民们发现不仅老槐树的影子不见了，连整个树干也消失得无影无踪，只剩下那个空荡的小洞穴静静躺在那里。\n\n经过几天的研究与讨论，一位有智慧的老者解释说，这可能是古老神灵为了警示人类不要过度干扰自然法则而采取的一种超自然手段。虽然老槐树消失了，但它的存在和传说依旧留在了村民们的心中，并且也使得这个小村庄的神秘色彩更浓重了。\n"
    result = taste_soup(
        truth=truth,
        style=style,
        character=character,
        setting=setting,
        theme=theme
    )
