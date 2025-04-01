import os
from openai import OpenAI
import base64

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-e4fc9036feea4c44ae5c099d3ccef0f8",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


#  Base64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("MinerU/images/1a0784a685310aaf96944ddba1a32094d57e84c0f0f33d4e38da95aa14d99f3b.jpg")

completion = client.chat.completions.create(
    model="qwen-omni-turbo",
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ],
        },
    ],
    # 设置输出数据的模态，当前支持["text"]
    modalities=["text"],
    # stream 必须设置为 True，否则会报错
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)