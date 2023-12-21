# utils.py
import requests
import json
import numpy as np
from typing import List, Tuple
import tempfile
import os

CHATGLM_API_ENDPOINT = "http://127.0.0.1:7861/"


#QA_PROMPT = '<指令>根据已知信息，确保你已理解相关内容，请以简洁和专业的语言，基于已知信息的内容，生成5个QA对，格式如下：Q:... A:...，.QA对请使用中文。 </指令>\n' \
#            '<已知信息>{{ context }}</已知信息>\n' \
#            '<问题>{{ question }}</问题>\n'

def make_question(text:str) -> str:
    return '根据以下文本，确保你已理解相关内容，请以简洁和专业的语言，基于已知信息的内容，生成5个问答对(Q&A)：' + text[:1000] + '请按照以下格式提供问答对: [{"Q1" : "问题1",  "A1" : "回答1"},\
            {"Q2" : "问题2",  "A2" : "回答2"},{"Q3" : "问题3",  "A3" : "回答3"},{"Q4" : "问题4",  "A4" : "回答4"},{"Q5" : "问题5",  "A5" : "回答5"}]。问题和回答之间使用换行进行间隔，生成5个问答对(Q&A)。'

# 从chatglm API获取Q&A对的函数
def get_qa_pairs(text):
    # Replace with the actual API endpoint and set up the request as needed
    url = CHATGLM_API_ENDPOINT + "chat/chat"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        "query": make_question(text),
        "conversation_id": "a",
        "history_len": -1,
        "history": [],
        "stream": False,
        "model_name": "chatglm2-6b",
        "temperature": 0.7,
        "max_tokens": 0,
        "prompt_name": "default"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    if response.status_code == 200:
        response_data = response.json()
        return response_data['text'] # Assuming the API returns a JSON with Q&A pairs
    else:
        return []


def upload_txt_to_knowledge_base(content_str: str, filename: str):
    # 在/tmp目录下创建一个临时文件
    tmp_dir = "./tmp"
    os.makedirs(tmp_dir, exist_ok=True)

    temp_file_path = os.path.join(tmp_dir, filename)
    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.write(content_str)

    url = CHATGLM_API_ENDPOINT + "knowledge_base/upload_docs"
    headers = {
        'accept': 'application/json',
    }

    # 打开文本文件进行读取
    with open(temp_file_path, 'rb') as txt_file:
        files = {
            'files': (filename, txt_file, 'text/plain')
        }

        data = {
            'to_vector_store': 'true',
            'override': 'true',
            'not_refresh_vs_cache': 'false',
            'chunk_size': '250',
            'chunk_overlap': '50',
            'zh_title_enhance': 'false',
            'knowledge_base_name': 'sales',
            'docs': json.dumps({
                filename: [
                    {
                        "page_content": content_str,
                        "metadata": {},
                        "type": "Document"
                    }
                ]
            })
        }

        response = requests.post(url, headers=headers, files=files, data=data)

    # 删除临时文件
    os.remove(temp_file_path)

    #if response.status_code == 200:
    #    return response.json()  # 操作成功，返回 JSON 数据
    #else:
    #    return response.text  # 操作失败，返回错误信息

    return response

def upload_pdf_to_knowledge_base(pdf_file):
    url = CHATGLM_API_ENDPOINT + "knowledge_base/upload_docs"

    # 准备 headers，根据你的服务器要求可能需要更多的 headers
    headers = {
        'accept': 'application/json',
    }

    # 准备表单数据
    files = {
        'files': (pdf_file.name, pdf_file, 'application/pdf')
    }

    data = {
        'to_vector_store': 'true',
        'override': 'true',
        'not_refresh_vs_cache': 'false',
        'chunk_size': '250',
        'chunk_overlap': '50',
        'zh_title_enhance': 'false',
        'knowledge_base_name': 'sales',
        'docs': json.dumps({
            "test.txt": [
                {
                    "page_content": "custom doc",
                    "metadata": {},
                    "type": "Document"
                }
            ]
        })
    }

    # 发起请求
    response = requests.post(url, headers=headers, files=files, data=data)

    #if response.status_code == 200:
    #    return response.json()  # 操作成功，返回 JSON 数据
    #else:
    #    return response.text  # 操作失败，返回错误信息

    return response


def get_knowledge_base_list_files():
    url = CHATGLM_API_ENDPOINT + "knowledge_base/list_files"
    params = {"knowledge_base_name": "sales"}
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", [])
        # 仅提取文件名而不是整个路径
        #file_names = [file.split("\\")[-1] for file in data]
        return data
    else:
        return []

# /knowledge_base/download_doc
def get_knowledge_base_file_content(file_name: str) -> str:
    url = CHATGLM_API_ENDPOINT + "knowledge_base/download_doc"
    params = {
        "knowledge_base_name": "sales",
        "file_name": file_name,
        "preview": "true"
    }
    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"请求失败，状态码：{response.status_code}")


# /other/embed_texts
def compare_text_similarity(text1: str, text2: str, embed_model: str = "m3e-base") -> float:
    """
    比较两个文本的相似度。
    """
    # 获取文本的嵌入向量
    embeddings = get_text_embeddings([text1, text2], embed_model)

    # 计算余弦相似度
    similarity = cosine_similarity(embeddings[0], embeddings[1])

    return similarity

def get_text_embeddings(texts: List[str], embed_model: str = "m3e-base", to_query: bool = False) -> List[List[float]]:
    """
    发送文本到接口并获取嵌入向量。
    """
    url = CHATGLM_API_ENDPOINT + "other/embed_texts"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "texts": texts,
        "embed_model": embed_model,
        "to_query": to_query
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"请求失败，状态码：{response.status_code}")

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量之间的余弦相似度。
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# /chat/knowledge_base_chat
def chat_with_knowledge_base(query: str,history) -> str:
    url = CHATGLM_API_ENDPOINT + "chat/knowledge_base_chat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "knowledge_base_name": "sales",
        "top_k": 3,
        "score_threshold": 1,
        "history": history,
        "stream": False,
        "model_name": "chatglm2-6b",
        "temperature": 0.7,
        "max_tokens": 0,
        "prompt_name": "default"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        raise Exception(f"请求失败，状态码：{response.status_code}，错误信息：{response.text}")

