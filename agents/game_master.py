from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from data_classes.answer import Answer
from data_classes.score import Score
# from generative_soup_agent import generative_loop
# from settings import LLM_MODEL, LLM
import re
from settings import getLLM

# 初始化模型
model="qwen3:14b"
temperature=0

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

async def question_master(
        soup: str,
        truth: str,
        question: str,
        result_holder: dict[str, Score | None], 
    ):
    llm = getLLM(model=model, temperature=temperature)
    
    answer_chain = answer_prompt | llm
    output_chunks = []

    async for event in answer_chain.astream_events({
        "soup": soup,
        "truth": truth,
        "question": question
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

    if isinstance(result, Answer):
        print("---parsed correct---")
        print("主持回答：", result)
    else:
        print("parsed FAILED")
        print("!!!---PYDANTIC PARSING FAILED---!!!")

    result_holder["parsed_result"] = result