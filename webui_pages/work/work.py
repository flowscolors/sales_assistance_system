import streamlit as st
from streamlit_chatbox import *
import requests
import json

chat_box = ChatBox()
class SessionState:
    def __init__(self):
        self.messages = []
        self.recommendations = []

# 在这里实现获取推荐回复的逻辑,现在回复使用以下默认值
def get_recommendations(messages):
    if len(messages) > 0:
        return ["I'm sorry, I don't know how to respond to that yet.But I will be ok soon."]
    return []

# 调用chatchat API，提供参数封装
def get_response(question):
    response = post_chat(
        query=question,
        knowledge_base_name="samples",
        top_k=3,
        score_threshold=1,
        history=st.session_state['session_state'].messages,
        stream=False,
        model_name="chatglm2-6b",
        temperature=0.7,
        local_doc_url=False
    )

    print(response.json())
    return response.json()

# 调用chatchat API，输入query，得到返回
def post_chat(query, knowledge_base_name, top_k, score_threshold, history, stream, model_name, temperature, local_doc_url):
    url = "http://127.0.0.1:7861/chat/knowledge_base_chat"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        "query": query,
        "knowledge_base_name": knowledge_base_name,
        "top_k": top_k,
        "score_threshold": score_threshold,
        "history": history,
        "stream": stream,
        "model_name": model_name,
        "temperature": temperature,
        "local_doc_url": local_doc_url
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response
def work_page():
    st.title('Work Page')

    if 'session_state' not in st.session_state:
        st.session_state['session_state'] = SessionState()
    session_state = st.session_state['session_state']

    for message in session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.chat_message("user").markdown(prompt)
        session_state.messages.append({"role": "user", "content": prompt})
        response = f"Echo: {prompt}"
        st.text("推荐回复:  " + str(get_recommendations(session_state.messages)))
        with st.chat_message("assistant"):
            st.markdown(response)
        session_state.messages.append({"role": "assistant", "content": response})
        session_state.recommendations = get_recommendations(session_state.messages)

