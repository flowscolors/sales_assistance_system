
# 智能销售辅助系统 
一个用于学习、考试和工作的智能销售辅助系统

## 页面 
- **Know**: 知识库页面，提供上传知识功能。 前端上传pdf，生成QA问题，根据QA问题，存储到知识库（pdf和qa都存）。
- **Learn**: 学习页面，提供学习相关功能。 选择具体知识库文档，获取内容，进行问答。
- **Exam**: 考试页面，提供考试相关功能。  选择具体知识库文档，根据回答，匹配相似度，给出得分。
- **Work**: 工作页面，提供工作相关功能。  根据知识库，基于用户提问，给出推荐回答。

## 在线演示地址
http://riversouth.xyz:8501

## 安装
本地运行
```shell
pip install streamlit
pip install PyPDF2
streamlit run main.py
```

Docker打包
```shell
docker build -t mystreamlit:0.1 .
```


```shell
 docker run -d -p 8501:8501 jiangnanshi/mystreamlit:0.1
```

Docker运行