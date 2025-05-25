import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streaming.run_streaming import (
    run_soup_analyzer_streaming,
    run_soup_maker_streaming,
    run_soup_taster_streaming,
    run_story_maker_streaming,
    run_story_remaker_streaming
)


import streamlit as st

st.title("🐢 海龟汤")

if st.button('🔁 重新开始'):
    st.session_state.step = "input"
    st.session_state.generated = False  # 重置生成标志
    st.session_state.game_info = {}
    st.session_state.user_input = {}
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

        with st.expander(label="🧠 海龟汤生成中..."):
            # 这里示意调用生成函数，实际用你的函数替换
            story = run_story_maker_streaming(style, character, setting, theme)
            score = run_soup_taster_streaming(style, character, setting, theme, story)
            reflection = run_soup_analyzer_streaming(style, character, setting, theme, story, score)
            story = run_story_remaker_streaming(style, character, setting, theme, story, score, reflection)
            soup = run_soup_maker_streaming(story)

        st.session_state.generated_story = story
        st.session_state.generated_soup = soup
        st.session_state.generated = True

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
    with st.chat_message("ai"):
        st.markdown("#### 海龟汤汤面")
        st.markdown(st.session_state.game_info.get('soup', "暂无汤面"))

    if prompt := st.chat_input("向主持人提问。"):
        with st.chat_message("user"):
            st.markdown(prompt)



# st.button(label="rerun", on_click={
#     st.rerun()
# })


# else: # ALL GOOD
#     # user_input = st.session_state.user_input

#     if prompt := st.chat_input("向主持人提问。"):
#         with st.chat_message("user"):
#             st.markdown(prompt)


# TODO: this is tester for soup taster
# prompt = st.chat_input("Say something")
# if prompt:
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     style="超自然"
#     character="村民"
#     setting="月圆之夜"
#     theme="猎奇"
#     truth = "月圆之夜，村民们都在熟睡中，李明却独自一人站在村头的老槐树下等朋友。这棵老槐树是村里最古老的树木之一，据说已经活了超过一百年，夜晚时它那淡淡的影子总是伴随着满月的光芒显得格外神秘。\n\n就在这棵树的旁边，有一个小洞穴，里面藏有村民们世代相传的一个秘密：每当月圆之夜，村里的长者便会进入这个小洞穴，向里面的古老神灵祈求安宁与丰收。李明的好友恰好是一位对这些传说充满好奇的年轻人，他打算在这一晚通过神秘的仪式召唤出老槐树中的精灵。\n\n然而，就在李明好友准备进行仪式的时候，一道奇异的光芒突然从地下冒出，紧接着，一股强大的力量将整棵树和周围的一切瞬间拉进了另一个维度。第二天早上，村民们发现不仅老槐树的影子不见了，连整个树干也消失得无影无踪，只剩下那个空荡的小洞穴静静躺在那里。\n\n经过几天的研究与讨论，一位有智慧的老者解释说，这可能是古老神灵为了警示人类不要过度干扰自然法则而采取的一种超自然手段。虽然老槐树消失了，但它的存在和传说依旧留在了村民们的心中，并且也使得这个小村庄的神秘色彩更浓重了。\n"
#     output = run_soup_taster_streaming(style, character, setting, theme, truth)
#     if output:
#         if isinstance(output, Score):
#             print("\nYESHSDAS\n")
    
# TODO: this is tester for soup maker
# prompt = st.chat_input("Say something")
# if prompt:
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     truth = "月圆之夜，村民们都在熟睡中，李明却独自一人站在村头的老槐树下等朋友。这棵老槐树是村里最古老的树木之一，据说已经活了超过一百年，夜晚时它那淡淡的影子总是伴随着满月的光芒显得格外神秘。\n\n就在这棵树的旁边，有一个小洞穴，里面藏有村民们世代相传的一个秘密：每当月圆之夜，村里的长者便会进入这个小洞穴，向里面的古老神灵祈求安宁与丰收。李明的好友恰好是一位对这些传说充满好奇的年轻人，他打算在这一晚通过神秘的仪式召唤出老槐树中的精灵。\n\n然而，就在李明好友准备进行仪式的时候，一道奇异的光芒突然从地下冒出，紧接着，一股强大的力量将整棵树和周围的一切瞬间拉进了另一个维度。第二天早上，村民们发现不仅老槐树的影子不见了，连整个树干也消失得无影无踪，只剩下那个空荡的小洞穴静静躺在那里。\n\n经过几天的研究与讨论，一位有智慧的老者解释说，这可能是古老神灵为了警示人类不要过度干扰自然法则而采取的一种超自然手段。虽然老槐树消失了，但它的存在和传说依旧留在了村民们的心中，并且也使得这个小村庄的神秘色彩更浓重了。\n"
#     output = run_soup_maker_streaming(truth)
#     if output:
#         if isinstance(output, Score):
#             print("\nYESHSDAS\n")

# TODO: this is tester for story maker
# prompt = st.chat_input("Say something")
# if prompt:
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     output = run_story_maker_streaming("悬疑", "医生", "医院", "爱情")
#     if output:
#         if isinstance(output, Score):
#             print("\nYESHSDAS\n")

# TODO: this is tester for story REmaker
# prompt = st.chat_input("Say something")
# if prompt:
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     output = run_story_remaker_streaming(
#         style="超自然",
#         character="村民",
#         setting="月圆之夜",
#         theme="猎奇",
#         truth="月圆之夜，村民们都在熟睡中，李明却独自一人站在村头的老槐树下等朋友。这棵老槐树是村里最古老的树木之一，据说已经活了超过一百年，夜晚时它那淡淡的影子总是伴随着满月的光芒显得格外神秘。\n\n就在这棵树的旁边，有一个小洞穴，里面藏有村民们世代相传的一个秘密：每当月圆之夜，村里的长者便会进入这个小洞穴，向里面的古老神灵祈求安宁与丰收。李明的好友恰好是一位对这些传说充满好奇的年轻人，他打算在这一晚通过神秘的仪式召唤出老槐树中的精灵。\n\n然而，就在李明好友准备进行仪式的时候，一道奇异的光芒突然从地下冒出，紧接着，一股强大的力量将整棵树和周围的一切瞬间拉进了另一个维度。第二天早上，村民们发现不仅老槐树的影子不见了，连整个树干也消失得无影无踪，只剩下那个空荡的小洞穴静静躺在那里。\n\n经过几天的研究与讨论，一位有智慧的老者解释说，这可能是古老神灵为了警示人类不要过度干扰自然法则而采取的一种超自然手段。虽然老槐树消失了，但它的存在和传说依旧留在了村民们的心中，并且也使得这个小村庄的神秘色彩更浓重了。\n",
#         score={
#                 "confusion": {
#                     "score": 8,
#                     "comment": "故事中包含了许多超自然元素，如神秘的光芒和消失的老槐树，这些都能引发读者的好奇心，想知道背后发生了什么。"
#                 },
#                 "coherence": {
#                     "score": 6,
#                     "comment": "故事整体有一定的逻辑性，但缺乏对一些关键点的详细解释，比如为何召唤精灵会导致树被拉入另一个维度，这一点可能让读者感到有些牵强。"
#                 },
#                 "creativity": {
#                     "score": 7,
#                     "comment": "故事结合了超自然元素和古老传说，展示了一个独特的神秘事件，但整体创意性还有提升空间，因为它依赖于常见的神秘传说元素。"
#                 },
#                 "engagement": {
#                     "score": 9,
#                     "comment": "整个故事情节紧凑，充满了悬念和超自然现象，能够很好地激发读者的提问欲望，特别是关于老槐树消失的原因及其背后的深层含义。"
#                 }
#             },
#         reflection={
#             "weakness": "故事的关键转折点（如消失的老槐树）缺乏足够的解释，显得有些牵强",
#             "strategy": "在关键转折点之前，加入更多铺垫或背景信息，详细说明为什么特定事件会导致这种超自然现象"
#         }
#     )
#     if output:
#         if isinstance(output, Story):
#             print("\nYESHSDAS\n")

# TODO: this is tester for soup taster
# prompt = st.chat_input("Say something")
# if prompt:
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     style="超自然"
#     character="村民"
#     setting="月圆之夜"
#     theme="猎奇"
#     truth = "月圆之夜，村民们都在熟睡中，李明却独自一人站在村头的老槐树下等朋友。这棵老槐树是村里最古老的树木之一，据说已经活了超过一百年，夜晚时它那淡淡的影子总是伴随着满月的光芒显得格外神秘。\n\n就在这棵树的旁边，有一个小洞穴，里面藏有村民们世代相传的一个秘密：每当月圆之夜，村里的长者便会进入这个小洞穴，向里面的古老神灵祈求安宁与丰收。李明的好友恰好是一位对这些传说充满好奇的年轻人，他打算在这一晚通过神秘的仪式召唤出老槐树中的精灵。\n\n然而，就在李明好友准备进行仪式的时候，一道奇异的光芒突然从地下冒出，紧接着，一股强大的力量将整棵树和周围的一切瞬间拉进了另一个维度。第二天早上，村民们发现不仅老槐树的影子不见了，连整个树干也消失得无影无踪，只剩下那个空荡的小洞穴静静躺在那里。\n\n经过几天的研究与讨论，一位有智慧的老者解释说，这可能是古老神灵为了警示人类不要过度干扰自然法则而采取的一种超自然手段。虽然老槐树消失了，但它的存在和传说依旧留在了村民们的心中，并且也使得这个小村庄的神秘色彩更浓重了。\n"
#     score = {
#         "confusion": {
#             "score": 8,
#             "comment": "故事中包含了许多超自然元素，如神秘的光芒和消失的老槐树，这些都能引发读者的好奇心，想知道背后发生了什么。"
#         },
#         "coherence": {
#             "score": 6,
#             "comment": "故事整体有一定的逻辑性，但缺乏对一些关键点的详细解释，比如为何召唤精灵会导致树被拉入另一个维度，这一点可能让读者感到有些牵强。"
#         },
#         "creativity": {
#             "score": 7,
#             "comment": "故事结合了超自然元素和古老传说，展示了一个独特的神秘事件，但整体创意性还有提升空间，因为它依赖于常见的神秘传说元素。"
#         },
#         "engagement": {
#             "score": 9,
#             "comment": "整个故事情节紧凑，充满了悬念和超自然现象，能够很好地激发读者的提问欲望，特别是关于老槐树消失的原因及其背后的深层含义。"
#         }
#     }
#     output = run_soup_analyzer_streaming(style, character, setting, theme, truth, score)
#     if output:
#         if isinstance(output, Reflection):
#             print("\nYESHSDAS\n")