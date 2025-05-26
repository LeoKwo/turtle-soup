import streamlit as st
from streaming.run_streaming import (
    run_soup_analyzer_streaming,
    run_soup_maker_streaming,
    run_soup_taster_streaming,
    run_story_maker_streaming,
    run_story_remaker_streaming,
    run_game_master
)
import streamlit as st
from few_shot.retriever import search_soup
from settings import random_story_elements

st.title("🐢 海龟汤")

# SETTINGS
USE_LLM = True

if st.button('🔙 重新开始'):
    st.session_state.step = "input"
    st.session_state.generated = False  # 重置生成标志
    st.session_state.game_info = {}
    st.session_state.user_input = {}
    st.session_state["messages"] = []
    st.rerun()



# 初始化状态
if "step" not in st.session_state:
    st.session_state.step = "input"
if "generated" not in st.session_state:
    st.session_state.generated = False
if "user_input" not in st.session_state:
    st.session_state.user_input = {}
if "game_info" not in st.session_state:
    st.session_state.game_info = {}
# Define session state messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def handle_soup_setting(style, character, setting, theme):
    st.session_state.user_input = {
        "style": style, 
        "character": character, 
        "setting": setting, 
        "theme": theme
    }
    st.session_state.step = "generating"
    st.session_state.generated = False  # 标记为未生成，准备生成
    st.rerun()
    

if st.session_state.step == "input":
    if st.button('🔀 系统选择随机主题'):
        style, character, setting, theme = random_story_elements()
        st.success(f"系统选择了：\n{style, character, setting, theme}")
        handle_soup_setting(style, character, setting, theme)
    with st.form(key="user_form"):
        st.markdown("### 请输入以下关键词：")
        
        style = st.text_input("故事风格（悬疑、科幻、超自然等）")
        character = st.text_input("角色类型（医生、村民、职员等）")
        setting = st.text_input("设定背景（末世、医院、皇宫等）")
        theme = st.text_input("故事主题（爱情、背叛、误会等）")
        submit_button = st.form_submit_button(label="🧠 开始生成")

        if submit_button:
            handle_soup_setting(style, character, setting, theme)
        

elif st.session_state.step == "generating":
    if not st.session_state.generated:
        user_input = st.session_state.user_input
        style, character, setting, theme = user_input.values()

        few_shot_examples = search_soup(query=f"{(style, character, setting, theme)}")

        if USE_LLM:
            with st.expander(label="🧠 海龟汤生成中..."):
                # # step 1: 生成汤底
                # story = run_story_maker_streaming(style, character, setting, theme)
                # # step 2: 品尝汤底
                # score = run_soup_taster_streaming(style, character, setting, theme, story)
                # # step 3: 计划改进
                # reflection = run_soup_analyzer_streaming(style, character, setting, theme, story, score)
                # # step 4：重做汤底
                # story = run_story_remaker_streaming(style, character, setting, theme, story, score, reflection, few_shot_examples)
                # # step 5: 生成汤面
                # soup = run_soup_maker_streaming(story)

                # ------------

                # step 1: 生成汤底
                story = run_story_maker_streaming(style, character, setting, theme, few_shot_examples)
                # step 5: 生成汤面
                soup = run_soup_maker_streaming(story)
                # step 2: 品尝汤底
                score = run_soup_taster_streaming(style, character, setting, theme, f"汤面：{soup}\n汤底: {story}")
                # step 3: 计划改进
                reflection = run_soup_analyzer_streaming(style, character, setting, theme, f"汤面：{soup}\n汤底: {story}", score)
                # step 4：重做汤底
                story = run_story_remaker_streaming(style, character, setting, theme, f"汤面：{soup}\n汤底: {story}", score, reflection, few_shot_examples)
                # step 5: 生成汤面
                soup = run_soup_maker_streaming(story)
                
            st.session_state.generated_story = story
            st.session_state.generated_soup = soup
            st.session_state.generated = True
        else:
            st.session_state.generated_story = """
                女士是杂技团的一名演员，那天她去买了一双红色的高跟鞋。
                晚上她穿着这双高跟鞋就去马 戏团上班了，她的工作是头顶
                苹果，配合另外一名男演员表演小李飞刀。结果因为她的高
                跟鞋，她比平时高出了几公分，没有调整过来的男演员失手将
                刀插到了她的脑袋上。"""
            st.session_state.generated_soup = "一位女士去鞋店里买了一双红色高跟鞋，这双高跟鞋预示了她今晚的死亡。"

    # 生成完毕后显示按钮，点击进入游戏
    if st.button('🕹️ 开始游戏'):
        st.session_state.game_info = {
            "soup": st.session_state.generated_soup,
            "story": st.session_state.generated_story
        }
        st.session_state.step = "playing"
        st.session_state.generated = False  # 清除生成标志
        st.rerun()

elif st.session_state.step == "playing":
    # render chat interface
    with st.container():
        st.markdown(body=f"#### 汤面\n{st.session_state.game_info.get('soup', '暂无汤面')}")

    # Write chat history to screen
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])

        else:
            st.chat_message("user").write(msg["content"])

    

    if question := st.chat_input("向主持人提问 ..."):            
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message(name="human").write(question)
        with st.chat_message(name="assistant"):
            response = run_game_master(story=st.session_state.game_info['story'], soup=st.session_state.game_info['soup'], question=question)
            st.session_state.messages.append({"role": "assistant", "content": response.answer})
            st.write(response.answer)
                