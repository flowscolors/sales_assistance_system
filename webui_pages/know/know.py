import streamlit as st
import requests
from PyPDF2 import PdfReader
from ..utils import get_qa_pairs, upload_pdf_to_knowledge_base, upload_txt_to_knowledge_base


# # 从PDF中提取文本的函数
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text


# 1.前端上传pdf，根据pdf内容解析生成文本。
# 2.根据文本，封装promots，调用chatglm api，生成5个QA问题。
# 3.根据QA对，存储到chatglm知识库（pdf和qa都存）
def know_page():
    st.title('Know Page')

    # 使用columns来并排放置按钮
    col1, col2 = st.columns(2)

    with col1:
        # “生成/刷新Q&A”按钮
        if st.button("生成/刷新Q&A"):
            if 'pdf_text' in st.session_state:
                # 从session_state重新获取QA对
                st.session_state['qa_pairs'] = get_qa_pairs(st.session_state['pdf_text'])

    with col2:
        # “保存Q&A到知识库”按钮
        # TODO 如何在这里保存pdf，也可以不存pdf
        # TODO 如何将qa对拆分成list的问答对
        if st.button("保存Q&A到知识库"):
            if 'qa_pairs' in st.session_state:
                # 在这里实现将Q&A保存到您的知识库的逻辑
                upload_txt_to_knowledge_base(st.session_state['qa_pairs'], "5-qa.txt")
                st.success("Q&A对已保存到知识库！")

    # 设置布局的列
    left_column, right_column = st.columns(2)

    # 左列用于PDF上传和文本显示
    with left_column:
        st.subheader("上传PDF")
        pdf_file = st.file_uploader("选择一个PDF文件", type="pdf")
        if pdf_file is not None:
            # 上传文件并获取响应
            response = upload_pdf_to_knowledge_base(pdf_file)
            st.write(response)

        st.session_state['pdf_file'] = pdf_file
        if pdf_file is not None:
            # 提取文本并存储在session_state中
            st.session_state['pdf_text'] = extract_text_from_pdf(pdf_file)
            st.subheader("提取的文本")
            st.write(st.session_state['pdf_text'])

    # 右列用于显示Q&A
    with right_column:
        st.subheader("生成的Q&A")
        if 'qa_pairs' in st.session_state:
            st.write(st.session_state['qa_pairs'])
    # if 'qa_pairs' in st.session_state:
    #     for qa in st.session_state['qa_pairs'][:5]:  # 显示前5个Q&A对
    #         st.text("Q: " + qa['question'])
    #         st.text("A: " + qa['answer'])
    #         st.write("---")
