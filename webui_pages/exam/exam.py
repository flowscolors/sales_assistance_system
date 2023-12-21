import streamlit as st
from streamlit_chatbox import *
import random
from ..utils import compare_text_similarity,get_knowledge_base_file_content

chat_box = ChatBox()

# 定义问答对
qa_pairs = {
    "什么是保险？": "保险是一种合同，由保单代表，其中个人或实体从保险公司获得对损失的经济保护或补偿。",
    "保险中的保费是什么？": "保费是您的保险公司为您选择的保险计划收取的金额，通常每月支付一次，但可以根据您的保险公司和您的具体保险类型以不同方式进行计费。",
    "保险中的免赔额是什么？": "免赔额是您在健康保险开始支付之前支付的医疗服务费用。",
    "什么是人寿保险？": "人寿保险是保单持有人和保险公司之间的合同，其中保险公司承诺在被保人死亡时向指定受益人支付一笔钱。",
    "什么是汽车保险？": "汽车保险是车主购买的保单，以降低因发生汽车事故而产生的费用。"
}

def calculate_score(query):
    # 在这里实现你的打分逻辑
    score = round(random.uniform(1, 100), 2)
    return score

def exam_page():
    st.title('Exam Page')
    print(compare_text_similarity("hello","world"))
    print(compare_text_similarity("11111", "11111"))
    print(compare_text_similarity("保险是一种合同，由保单代表，其中个人或实体从保险公司获得对损失的经济保护或补偿。", "保险是一种合同，由保单代表，其中个人或实体从保险公司获得对损失的经济保护或补偿。"))

    print(get_knowledge_base_file_content("F:\\project\\Langchain-Chatchat\\knowledge_base\\samples\\content\\test_files\\test.txt"))
    chat_box.init_session()  # 初始化会话

    # 初始化 session state
    if 'qa_index' not in st.session_state:
        st.session_state.qa_index = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = []

    # 获取问题和答案
    questions = list(qa_pairs.keys())
    answers = list(qa_pairs.values())

    # 开始问答
    if st.session_state.qa_index < len(questions):
        chat_box.ai_say("问题" + str(st.session_state.qa_index+1) + "： " + questions[st.session_state.qa_index])
        if query := st.chat_input('input your answer here'):
            chat_box.user_say(query)
            score = calculate_score(query)
            chat_box.ai_say("得分： " + str(score))
            chat_box.ai_say("正确答案是： " + answers[st.session_state.qa_index])
            st.session_state.scores.append(score)
            st.session_state.qa_index += 1

            if st.session_state.qa_index <= len(questions):
                if st.button("下一题"):
                    pass

    else:
        chat_box.ai_say("考试结束")
        st.write("每题得分：")
        for i, score in enumerate(st.session_state.scores):
            st.write("问题" + str(i+1) + "得分：" + str(score))
        average_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.write("考试总分：" + str(average_score))
