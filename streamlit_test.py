import streamlit as st
from data_classes.score import Score
from data_classes.reflection import Reflection
from data_classes.soup import Soup
from data_classes.soup import Story
import re
from agents.soup_taster_stream import taste_soup
from agents.soup_maker_stream import make_soup
from agents.story_maker_stream import make_story
from agents.soup_analyst_stream import analyze_soup
from run_streaming import (
    run_soup_analyzer_streaming,
    run_soup_maker_streaming,
    run_soup_taster_streaming,
    run_story_maker_streaming,
    run_story_remaker_streaming
)

# def run_llm_with_retries(func, *args, **kwargs):
#     for attempt in range(1, 4):
#         try:
#             print(f"Attempt {attempt}...")
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f"Error on attempt {attempt}: {e}")
#             if attempt == 3:
#                 raise

st.title("🐢 海龟汤")

# State to store whether the form has been submitted
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# State to store whether the story is ready
# if "ready" not in st.session_state:
#     st.session_state.ready = False

# State to store form data
if "user_input" not in st.session_state:
    st.session_state.user_input = {}

# State to store game info
if "game_info" not in st.session_state:
    st.session_state.game_info = {}

def handle_soup_setting(style, character, setting, theme):
    st.session_state.submitted = True
    st.session_state.user_input = {
        "style": style, 
        "character": character, 
        "setting": setting, 
        "theme": theme
    }

# def handle_game_start(soup, story):
#     st.session_state.ready = True
#     st.session_state.game_info = {
#         "soup": soup,
#         "story": story
#     }
    # st.rerun()

# print(f"\n\n{st.session_state.submitted, st.session_state.ready}")

if not st.session_state.submitted:
    with st.form(key="user_form"):
        st.markdown("### 请输入以下关键词：")
        style = st.text_input("故事风格（悬疑、科幻、超自然等）")
        character = st.text_input("角色类型（医生、村民、职员等）")
        setting = st.text_input("设定背景（末世、医院、皇宫等）")
        theme = st.text_input("故事主题（爱情、背叛、误会等）")
        submit_button = st.form_submit_button(label="冲")

        if submit_button:
            handle_soup_setting(style, character, setting, theme)
else:
    user_input = st.session_state.user_input
    style, character, setting, theme = user_input.values()
    with st.expander(label="🧠 海龟汤生成中..."):
        story = run_story_maker_streaming(style, character, setting, theme)
        score = run_soup_taster_streaming(style, character, setting, theme, story)
        reflection = run_soup_analyzer_streaming(style, character, setting, theme, story, score)
        story = run_story_remaker_streaming(style, character, setting, theme, story, score, reflection)
        soup = run_soup_maker_streaming(story)
        # start_game_button = st.button(label="🕹️ 开始游戏")
        
        # st.session_state.ready = True
        # st.rerun()
        # if start_game_button:
            # st.session_state.ready = True
    st.session_state.game_info = {
        "soup": soup,
        "story": story
    }
            # st.rerun()
            # handle_game_start(soup, story)
            # handle_game_start("", story)
    
    with st.chat_message("ai"):
        st.markdown("#### 海龟汤汤面")
        st.markdown(st.session_state.game_info['soup'])
    if prompt := st.chat_input("向主持人提问。"):

        with st.chat_message("user"):
            st.markdown(prompt)
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