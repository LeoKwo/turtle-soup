from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_community.chat_models import ChatZhipuAI
import os
import random
load_dotenv()

# LLM_MODEL = "qwq:latest" # 32b (20G)
LLM_MODEL = "qwen3:30b" # 19G
def getLLM(model=LLM_MODEL, temperature=0.9):
    return ChatOllama(model=model, temperature=temperature)

# LLM_MODEL = "deepseek-reasoner"
# def getLLM(model=LLM_MODEL, temperature=0.9):
#     return ChatDeepSeek(model=model, temperature=temperature, streaming=True)

# LLM_MODEL = "GLM-Z1-Air"
# def getLLM(model=LLM_MODEL, temperature=0.9):
#     return ChatZhipuAI(model=model, temperature=temperature, streaming=True)


EMBED_MODEL = "herald/dmeta-embedding-zh"
def getEMBED(model=EMBED_MODEL):
    return OllamaEmbeddings(model=EMBED_MODEL)

seeds = {
    "故事风格": [
        "悬疑惊悚", "温情治愈", "荒诞黑色", "社会派推理",
        "奇幻寓言", "现实主义", "浪漫主义", "冷硬派",
        "青春物语", "家庭伦理", "历史戏说", "科幻隐喻",
        "心理剖析", "犯罪纪实", "魔幻现实", "成长叙事"
    ],
    
    "角色类型": [
        "普通上班族", "退休老人", "叛逆少年", "神秘访客",
        "失忆患者", "乡村教师", "流浪艺人", "医护人员",
        "餐馆老板", "图书管理员", "出租车司机", "建筑工人",
        "单亲家长", "退伍军人", "大学生", "自由职业者"
    ],
    
    "设定背景": [
        "暴雨中的小镇", "深夜末班车", "废弃工厂", "老旧社区",
        "山区民宿", "海边渔村", "城市地铁站", "乡村小学",
        "冬季滑雪场", "夏季庙会", "跨年晚会", "清晨菜市场",
        "深夜便利店", "长途列车", "建筑工地", "社区医院"
    ],
    
    "故事主题": [
        "身份认同", "记忆迷局", "谎言漩涡", "意外重逢",
        "命运巧合", "秘密守护", "道德困境", "自我救赎",
        "亲情羁绊", "信任危机", "时间循环", "物品诅咒",
        "集体沉默", "谣言传播", "意外目击", "身份互换"
    ]
}

def random_story_elements(story_dict=seeds):
    """
    随机返回故事创作四要素
    :param story_dict: 包含四个分类的字典
    :return: (风格, 角色, 背景, 主题) 的元组
    """
    return (
        random.choice(story_dict["故事风格"]),
        random.choice(story_dict["角色类型"]),
        random.choice(story_dict["设定背景"]),
        random.choice(story_dict["故事主题"])
    )