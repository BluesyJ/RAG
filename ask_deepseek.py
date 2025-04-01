from openai import OpenAI
from typing import List, Dict
import os
import time
class DeepSeekChat:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.dialog_history = []

    def load_document(self, md_file_path: str):
        """加载Markdown文档到系统消息"""
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 初始化系统消息
            self.dialog_history = [
                {
                    "role": "system",
                    "content": f"基于以下文档内容回答问题：\n{md_content}"
                },
                {
                    "role": "assistant", 
                    "content": "文档已加载完成，请开始提问。"
                }
            ]
            print("文档加载成功！输入 'exit' 结束对话\n")
            self._print_last_message()

        except Exception as e:
            print(f"文档加载失败: {str(e)}")
            raise

    def _print_last_message(self):
        if self.dialog_history:
            last_msg = self.dialog_history[-1]
            print(f"[{last_msg['role']}]: {last_msg['content']}\n")

    def chat_loop(self):
        try:
            while True:
                user_input = input("[用户]: ").strip()
                if user_input.lower() in ['exit', '退出']:
                    break
                
                start_time = time.time()
                self.dialog_history.append({"role": "user", "content": user_input})
                
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=self.dialog_history,
                    temperature=1.0,
                    max_tokens=2000
                )
                
                assistant_msg = response.choices[0].message
                self.dialog_history.append({
                    "role": "assistant",
                    "content": assistant_msg.content
                })
                end_time = time.time()
                print(f"[助手]: {assistant_msg.content}\n")
                print(f"耗时: {end_time - start_time:.2f}秒\n")

        except KeyboardInterrupt:
            print("\n对话已终止")
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    API_KEY = "sk-22146a806dcf42b68ab12ae2d4ddee7d" 
    MD_FILE = "Titanic.txt"
    
    # 初始化聊天实例
    ds_chat = DeepSeekChat(API_KEY)
    
    try:
        ds_chat.load_document(MD_FILE)
        ds_chat.chat_loop()
    except Exception as e:
        print(f"程序异常终止: {str(e)}")