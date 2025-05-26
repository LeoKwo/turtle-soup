# Turtle Soup Game
Agentic LLM Turtle Soup Game. Dynamically generate turtle soup stories.

### What is a turtle soup game?
Read more here: [https://en.wikipedia.org/wiki/Situation_puzzle](https://en.wikipedia.org/wiki/Situation_puzzle)

### Requirements
1. Ollama
2. LangChain
3. Streamlit
4. Qwen3

### Features
1. Support for reasoning models such as Qwen3 and DeepSeek-R1
2. Support for streaming LLM output to Streamlit UI

### To-dos
1. Game master needs the ability to know if the user has reached the final truth
2. Implement a save and load feature for generated stories

### Installation
1. ```ollama pull qwen3:30b``` ```ollama pull qwen3:14b```. You can change to whatever LLM that fits in your VRAM
2. ```pip install -r requirements.txt``` Install dependencies
3. ```streamlit run turtle_soup.py``` to start game!

### System Requirements
- A beefy graphics card
    - I am using an AMD RX 7900 XT with 20 GB VRAM. It can barely hold Qwen3:30b.
    - You can try models with lower quant but the quality drops significantly.
- You may choose to go with online models for the best performance