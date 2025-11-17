import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://api.deepseek.com")

def judge_level(text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
            {"role": "user", "content": text},
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def tiao_zheng(text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "### 定位：语言表述专家\n ### 任务：将歧视性语句换一种方法表述，使表述中不包含歧视语义。"},
            {"role": "user", "content": text},
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

st.set_page_config(page_title='fff')
st.title("语言检测及纠正🎶")
user_input = st.text_area('请输入要分析的句子：', height=100)
if st.button('开始分析'):
    if user_input.strip() == '':
        st.warning("请输入有效内容")
    else:
        st.spinner('正在分析中...', show_time=True)：
        score = judge_level(user_input)
        st.success(f'歧视分析结果得分是：**{score}**')
        if score != '1':
            result = tiao_zheng(user_input)
            st.success(f'调整后的语句是：**{result}**')

