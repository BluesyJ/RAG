import re
import os
import base64
from openai import OpenAI

def describe_image(image_path):
    client = OpenAI(
        api_key="sk-e4fc9036feea4c44ae5c099d3ccef0f8",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    base64_image = encode_image(image_path)

    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=[
            {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ]},
        ]
    )

    return completion.choices[0].message.content if completion.choices else "图片描述生成失败"
def replace_image_links(markdown_file, image_folder, output_file):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 匹配Markdown图片链接
    image_links = re.findall(r'!\[.*?\]\((.*?)\)', content)

    # 替换每个图片链接
    for link in image_links:
        image_path = os.path.join(image_folder, os.path.basename(link))
        if os.path.exists(image_path):
            description = describe_image(image_path)
            content = content.replace(f'![]({link})', f'[图片描述：{description}]')

    # 输出结果
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"转换完成！已保存到 {output_file}")

if __name__ == "__main__":
    input_file_fold = "D:/SYJProject/RAG/mineru_result/20250326"
    markdown_file = os.path.join(input_file_fold, "document.md")
    image_folder = os.path.join(input_file_fold, "images")      # 图片所在的文件夹
    output_file = os.path.join(input_file_fold, "output.md")     # 输出Markdown文件路径

    replace_image_links(markdown_file, image_folder, output_file)
