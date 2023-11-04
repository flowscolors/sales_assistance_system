import streamlit as st

from webui_pages import learn, exam, work

PAGES = {
    "Learn": learn.learn_page,
    "Exam": exam.exam_page,
    "Work": work.work_page
}

def main():

    st.sidebar.title('智能销售辅助系统')  # toast 欢迎消息
    st.sidebar.caption('版本：1.0.0')  # 显示版本号
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()