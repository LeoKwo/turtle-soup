import streamlit as st
from data_classes.score import Score
from data_classes.reflection import Reflection
from data_classes.soup import Soup
from data_classes.soup import Story
from data_classes.answer import Answer
import re
from agents.soup_taster_stream import taste_soup
from agents.soup_maker_stream import make_soup
from agents.story_maker_stream import make_story
from agents.story_remaker_stream import remake_story
from agents.soup_analyst_stream import analyze_soup
from agents.game_master import question_master

def run_soup_analyzer_streaming(style, character, setting, theme, truth, score: Score) -> Reflection | None:
    result_holder: dict[str, Reflection | None] = {}
    full_output_holder = {"text": ""}

    # 1️⃣ Use placeholder for the streaming message
    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.chat_message("ai"):
            async def wrapper_gen():
                async for chunk in analyze_soup(
                    style, character, setting, theme, truth, score,
                    result_holder=result_holder
                ):
                    full_output_holder["text"] += chunk
                    yield chunk
                

            st.write_stream(wrapper_gen)

    # 2️⃣ Once streaming is done, clear the placeholder
    streaming_placeholder.empty()

    # 3️⃣ Extract and display structured output
    full_output = full_output_holder["text"]

    # Extract <think>...</think>
    think_match = re.search(r"<think>(.*?)</think>", full_output, re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""

    # Remove <think>...</think> and <think/> from final output
    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    # 4️⃣ Render final version
    with st.chat_message("ai"):
        if think_text:
            with st.popover("**💭 海龟汤改进建议**"):
                st.markdown(think_text)
        st.markdown(main_output)
    return result_holder.get("parsed_result")

def run_story_maker_streaming(style, character, setting, theme) -> Story | None:
    result_holder: dict[str, Story | None] = {}
    full_output_holder = {"text": ""}

    # 1️⃣ Use placeholder for the streaming message
    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.chat_message("ai"):
            async def wrapper_gen():
                async for chunk in make_story(
                    style, character, setting, theme,
                    result_holder=result_holder
                ):
                    full_output_holder["text"] += chunk
                    yield chunk

            st.write_stream(wrapper_gen)

    # 2️⃣ Once streaming is done, clear the placeholder
    streaming_placeholder.empty()

    # 3️⃣ Extract and display structured output
    full_output = full_output_holder["text"]

    # Extract <think>...</think>
    think_match = re.search(r"<think>(.*?)</think>", full_output, re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""

    # Remove <think>...</think> and <think/> from final output
    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    # 4️⃣ Render final version
    with st.chat_message("ai"):
        if think_text:
            with st.popover("**💭 完整的海龟汤故事**"):
                st.markdown(think_text)
        st.markdown(main_output)

    return result_holder.get("parsed_result")

def run_story_remaker_streaming(style, character, setting, theme, truth, score: Score, reflection: Reflection) -> Story | None:
    result_holder: dict[str, Story | None] = {}
    full_output_holder = {"text": ""}

    # 1️⃣ Use placeholder for the streaming message
    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.chat_message("ai"):
            async def wrapper_gen():
                async for chunk in remake_story(
                    style, character, setting, theme, truth, score, reflection,
                    result_holder=result_holder
                ):
                    full_output_holder["text"] += chunk
                    yield chunk

            st.write_stream(wrapper_gen)

    # 2️⃣ Once streaming is done, clear the placeholder
    streaming_placeholder.empty()

    # 3️⃣ Extract and display structured output
    full_output = full_output_holder["text"]

    # Extract <think>...</think>
    think_match = re.search(r"<think>(.*?)</think>", full_output, re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""

    # Remove <think>...</think> and <think/> from final output
    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    # 4️⃣ Render final version
    with st.chat_message("ai"):
        if think_text:
            with st.popover("**💭 改写的海龟汤故事**"):
                st.markdown(think_text)
        st.markdown(main_output)

    return result_holder.get("parsed_result")

def run_soup_maker_streaming(truth) -> Soup | None:
    result_holder: dict[str, Soup | None] = {}
    full_output_holder = {"text": ""}

    # 1️⃣ Use placeholder for the streaming message
    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.chat_message("ai"):
            async def wrapper_gen():
                async for chunk in make_soup(
                    truth=truth,
                    result_holder=result_holder
                ):
                    full_output_holder["text"] += chunk
                    yield chunk

            st.write_stream(wrapper_gen)

    # 2️⃣ Once streaming is done, clear the placeholder
    streaming_placeholder.empty()

    # 3️⃣ Extract and display structured output
    full_output = full_output_holder["text"]

    # Extract <think>...</think>
    think_match = re.search(r"<think>(.*?)</think>", full_output, re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""

    # Remove <think>...</think> and <think/> from final output
    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    # 4️⃣ Render final version
    with st.chat_message("ai"):
        if think_text:
            with st.popover("**💭 海龟汤汤面**"):
                st.markdown(think_text)
        st.markdown(main_output)

    return result_holder.get("parsed_result")

def run_soup_taster_streaming(style, character, setting, theme, truth) -> Score | None:
    result_holder: dict[str, Score | None] = {}
    full_output_holder = {"text": ""}

    # 1️⃣ Use placeholder for the streaming message
    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.chat_message("ai"):
            async def wrapper_gen():
                async for chunk in taste_soup(
                    style=style,
                    character=character,
                    setting=setting,
                    theme=theme,
                    truth=truth,
                    result_holder=result_holder
                ):
                    full_output_holder["text"] += chunk
                    yield chunk

            st.write_stream(wrapper_gen)

    # 2️⃣ Once streaming is done, clear the placeholder
    streaming_placeholder.empty()

    # 3️⃣ Extract and display structured output
    full_output = full_output_holder["text"]

    # Extract <think>...</think>
    think_match = re.search(r"<think>(.*?)</think>", full_output, re.DOTALL)
    think_text = think_match.group(1).strip() if think_match else ""

    # Remove <think>...</think> and <think/> from final output
    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    # 4️⃣ Render final version
    with st.chat_message("ai"):
        if think_text:
            # with st.container():
            with st.popover(label="**💭 海龟汤评分**"):
                st.markdown(think_text)
        st.markdown(main_output)

    return result_holder.get("parsed_result")


def run_game_master(story: Story, question: str) -> Answer | None:
    result_holder: dict[str, Story | None] = {}
    full_output_holder = {"text": ""}

    streaming_placeholder = st.empty()

    with streaming_placeholder.container():
        with st.chat_message("ai"):
            async def wrapper_gen():
                async for chunk in question_master(
                    story, question,
                    result_holder=result_holder
                ):
                    full_output_holder["text"] += chunk
                    yield chunk

            st.write_stream(wrapper_gen)

    streaming_placeholder.empty()

    full_output = full_output_holder["text"]

    # think_match = re.search(r"<think>(.*?)</think>", full_output, re.DOTALL)
    # think_text = think_match.group(1).strip() if think_match else ""

    main_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)
    main_output = re.sub(r"<think\s*/>", "", main_output).strip()

    with st.chat_message("ai"):
        # if think_text:
        #     with st.popover("**💭 改写的海龟汤故事**"):
        #         st.markdown(think_text)
        st.markdown(main_output)

    return result_holder.get("parsed_result")