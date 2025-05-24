import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
from soup_maker import make_soup
from soup_taster import taste_soup
from data_classes.answer import Answer
from data_classes.score import Score
from generative_soup_agent import generative_loop
# from settings import LLM_MODEL, LLM
from settings import getLLM

# 初始化模型
llm = getLLM(model="qwen3:14b", temperature=0)

def get_question():
    question = input("向主持人提问：")
    return question

# 输出模版
outputParser = PydanticOutputParser(pydantic_object=Answer)

answer_prompt = PromptTemplate.from_template("""
    你是一位擅长主持海龟汤游戏的主持人。

    以下是本轮海龟汤的汤面与汤底：
    【汤面】：{soup}
    【真相】：{truth}

    玩家本轮的问题：
    {question}
                                 
    请根据汤底的故事真相，回答用户的问题。
    注意！只能回答“是”，“否”，或者“不相关”。

    请用以下 JSON 格式回复：
    {{
        "answer": "请根据汤底的故事真相，回答用户的问题。只能回答“是”，“否”，或者“不相关”。"
    }}
""")

def game_master(
        soup: str,
        truth: str,
        question: str
    ):
    
    answer_chain = answer_prompt | llm | outputParser

    result = answer_chain.invoke({
        "soup": soup,
        "truth": truth,
        "question": question
    })

    if isinstance(result, Answer):
        print("---parsed correct---")
        print("主持回答：", result)
    else:
        print("parsed FAILED")
        print("!!!---PYDANTIC PARSING FAILED---!!!")
        
    
if __name__ == "__main__":
    soup, truth = generative_loop()
    while True:
        question = get_question()
        game_master(soup, truth, question)