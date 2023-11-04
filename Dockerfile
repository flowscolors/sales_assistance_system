# 使用官方的Python基础镜像
FROM python:3.8-slim-buster

# 工作目录设置为/app
WORKDIR /app

# 将当前目录文件添加到工作目录/app中
ADD . /app

# 安装在streamlit、streamlit-chatbox
RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple streamlit
RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple streamlit-chatbox

# 镜像启动后执行的命令
CMD streamlit run main.py