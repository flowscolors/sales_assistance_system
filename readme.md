
# 智能销售辅助系统 一
个用于学习、考试和工作的智能销售辅助系统

## 页面 
- **Learn**: 学习页面，提供学习相关功能。 目前使用Fake数据，后续接入chatchat知识库。
- **Exam**: 考试页面，提供考试相关功能。  目前使用Fake数据，后续接入chatchat知识库。
- **Work**: 工作页面，提供工作相关功能。  目前使用Fake数据，后续使用chatchat API。

## 在线演示地址
http://riversouth.xyz:8501

## 安装
本地运行
```shell
pip install streamlit
streamlit run main.py
```

Docker打包
```shell
docker build -t mystreamlit:0.1 .
```


Docker运行
```shell
 docker run -d -p 8501:8501 jiangnanshi/mystreamlit:0.1
```
