import streamlit as st
from streamlit_chatbox import *
import random
from ..utils import compare_text_similarity,get_knowledge_base_file_content,get_knowledge_base_list_files

chat_box = ChatBox()

# 定义问答对
qa_pairs = {
    "什么是保险？": "保险是一种合同，由保单代表，其中个人或实体从保险公司获得对损失的经济保护或补偿。",
    "保险中的保费是什么？": "保费是您的保险公司为您选择的保险计划收取的金额，通常每月支付一次，但可以根据您的保险公司和您的具体保险类型以不同方式进行计费。",
    "保险中的免赔额是什么？": "免赔额是您在健康保险开始支付之前支付的医疗服务费用。",
    "什么是人寿保险？": "人寿保险是保单持有人和保险公司之间的合同，其中保险公司承诺在被保人死亡时向指定受益人支付一笔钱。",
    "什么是汽车保险？": "汽车保险是车主购买的保单，以降低因发生汽车事故而产生的费用。"
}

def calculate_score(query,answer):
    # 在这里实现你的打分逻辑
    # score = round(random.uniform(1, 100), 2)
    # print(compare_text_similarity("hello", "world"))

    score = compare_text_similarity(query, answer)
    return round(score * 100, 2)

def extract_qa_pairs(text):
    # 分割字符串以获取独立的QA对，直接以换行进行分割
    qa_list = text.split('\r\n')
    print("qa_list :")
    print(qa_list)
    qa_pairs = {}

    # 遍历列表，跳过空字符串，并提取QA对
    for i in range(0, len(qa_list), 3):  # 步长为3，因为每个Q和A之后跟着一个空字符串
        question = qa_list[i].split(': ')[1].strip()  # 提取问题文本
        answer = qa_list[i + 1].split(': ')[1].strip()  # 提取答案文本
        qa_pairs[question] = answer

    return qa_pairs

def exam_page():
    st.title('Exam Page')

    # 在页面最上方添加一个下拉框
    BASE_DIR = "F:\\project\\Langchain-Chatchat\\knowledge_base\\sales\\content\\"
    dropdown_options = get_knowledge_base_list_files()
    filtered_options = [option for option in dropdown_options if option.endswith('5-qa.txt')]

    if filtered_options:
        selected_option = st.selectbox("选择一个文件", options=filtered_options)
        # print(selected_option)

        text = get_knowledge_base_file_content(BASE_DIR + selected_option)
        # print(text)
        # 使用函数提取QA对
        qa_pairs = extract_qa_pairs(text)
        print(qa_pairs)

    chat_box.init_session()  # 初始化会话

    # 初始化 session state
    if 'exam_index' not in st.session_state:
        st.session_state.exam_index = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = []

    # 获取问题和答案
    questions = list(qa_pairs.keys())
    answers = list(qa_pairs.values())

    # 开始问答
    if st.session_state.exam_index < len(questions):
        chat_box.ai_say("问题" + str(st.session_state.exam_index+1) + "： " + questions[st.session_state.exam_index])
        if query := st.chat_input('input your answer here'):
            chat_box.user_say(query)
            score = calculate_score(query,answers[st.session_state.exam_index])
            chat_box.ai_say("得分： " + str(score))
            chat_box.ai_say("正确答案是： " + answers[st.session_state.exam_index])
            st.session_state.scores.append(score)
            st.session_state.exam_index += 1

            if st.session_state.exam_index <= len(questions):
                if st.button("下一题"):
                    pass

    else:
        chat_box.ai_say("考试结束")
        st.write("每题得分：")
        for i, score in enumerate(st.session_state.scores):
            st.write("问题" + str(i+1) + "得分：" + str(score))
        average_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.write("考试总分：" + str(average_score))
