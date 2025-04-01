import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-e4fc9036feea4c44ae5c099d3ccef0f8",  # 如果没有配置环境变量，请替换API-KEY
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # DashScope服务base_url
)

# 用于总结每个文件块的函数
def summarize_chunk(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 向大模型请求总结
    completion = client.chat.completions.create(
        model="qwen-long",
        messages=[
            {'role': 'system', 'content': '你是一名专业的技术文档编辑,擅长对Markdown章节生成简明扼要的摘要'},
            {'role': 'user', 'content': f"请阅读以下Markdown文本，为该章节编写一段简洁、清晰的章节概述,要求仅保留关键主题、核心内容和主要信息点，避免冗长的解释和细节：\n\n{content}"}
        ],
        stream=False  # 非流式返回
    )

    # 获取总结结果
    summary = ""
    if completion.choices and completion.choices[0].message.content:
        summary = completion.choices[0].message.content

    return summary

# 合并多个文件块的总结
def summarize_and_store_chunks(chunk_dir, output_file):
    all_summaries = []

    # 获取所有Markdown文件（块）
    chunk_files = [f for f in os.listdir(chunk_dir) if f.endswith('.md')]
    
    for chunk_file in chunk_files:
        chunk_path = os.path.join(chunk_dir, chunk_file)
        summary = summarize_chunk(chunk_path)
        all_summaries.append(f"### {chunk_file}\n{summary}\n")

    # 合并所有总结
    full_summary = "\n".join(all_summaries)

    # 将合并后的总结写入到一个文件
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(full_summary)

    print(f"总结已保存到：{output_file}")

# 使用示例
chunk_directory = 'output'  # 替换为存储Markdown文件的目录
output_file = 'knowledge_graph_summary.md'  # 输出总结文件的路径

summarize_and_store_chunks(chunk_directory, output_file)
