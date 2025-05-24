from langchain_ollama.llms import OllamaLLM
from soup_maker import make_soup
from story_maker import make_story, remake_story
from soup_taster import taste_soup
from soup_analyst import analyze_soup

# from formats.score import Score

# 初始化模型
# llm = LLM

# 获取关键词
def get_user_keywords():
    print("请输入以下关键词：")
    style = input("故事风格：") or "随机风格"
    character = input("角色类型：") or "随机角色"
    setting = input("场景背景：") or "随机背景"
    theme = input("故事主题：") or "随机故事"
    return style, character, setting, theme

def generative_loop(n_cycles=2):

    style, character, setting, theme = get_user_keywords()

    truth, score, reflection = None, None, None

    for i in range(n_cycles):

        print(f"\n🌀 === Cycle {i+1} ===")

        
        if score is None: # 1st run
            truth = make_story(style, character, setting, theme)
            print(f"\nTruth:\n{truth}")
        else: # subsequent runs
            truth = remake_story(style, character, setting, theme, truth, score, reflection)
            print(f"\nTruth (Remake):\n{truth}")

        score = taste_soup(style, character, setting, theme, truth)
        print(f"\n📊 Score:\n{score}")

        
        reflection = analyze_soup(style, character, setting, theme, truth, score)

        print(f"\n🧠 Reflection: {reflection.weakness}")
        print(f"🛠️ Strategy for next prompt: {reflection.strategy}")

    soup = make_soup(truth)
    print(f"\n🍲 Soup:\nSurface: {soup.start} {soup.end}")
    
    return soup, truth

if __name__ == "__main__":
    soup, truth = generative_loop()