import streamlit as st
from streamlit_chatbox import *

chat_box = ChatBox()

# 定义问答对
qa_pairs = {
    "什么是保险？": "保险是一种合同，由保单代表，其中个人或实体从保险公司获得对损失的经济保护或补偿。",
    "保险中的保费是什么？": "保费是您的保险公司为您选择的保险计划收取的金额，通常每月支付一次，但可以根据您的保险公司和您的具体保险类型以不同方式进行计费。",
    "保险中的免赔额是什么？": "免赔额是您在健康保险开始支付之前支付的医疗服务费用。",
    "什么是人寿保险？": "人寿保险是保单持有人和保险公司之间的合同，其中保险公司承诺在被保人死亡时向指定受益人支付一笔钱。",
    "什么是汽车保险？": "汽车保险是车主购买的保单，以降低因发生汽车事故而产生的费用。"
}

def learn_page():
    st.title('Learn Page')
    chat_box.init_session()  # 初始化会话

    # 初始化 session state
    if 'qa_index' not in st.session_state:
        st.session_state.qa_index = 0

    # 获取问题和答案
    questions = list(qa_pairs.keys())
    answers = list(qa_pairs.values())

    # 开始问答
    if st.session_state.qa_index < len(questions):
        chat_box.ai_say("问题" + str(st.session_state.qa_index+1) + "： " + questions[st.session_state.qa_index])
        if query := st.chat_input('input your answer here'):
            chat_box.user_say(query)
            chat_box.ai_say("正确答案是： " + answers[st.session_state.qa_index])
            st.session_state.qa_index += 1

            if st.session_state.qa_index <= len(questions):
                if st.button("下一题"):
                    pass

    else:
        chat_box.ai_say("问答结束")
        if st.button("重新练习"):
            st.session_state.qa_index = 0

