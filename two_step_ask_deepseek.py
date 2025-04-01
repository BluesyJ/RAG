import os
import time
from openai import OpenAI

class DeepSeekChat:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def load_summary(self, summary_file: str):
        """加载章节概要，并存储为字典"""
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self.section_summaries = {
                    item.split("\n")[0].strip(): item.strip() 
                    for item in content.split("\n\n")
                }
            print("✅ 章节概要已加载！")
        except Exception as e:
            print(f"❌ 概要加载失败: {str(e)}")
            raise

    def get_relevant_section(self, question: str) -> str:
        """通过大模型筛选出最相关的章节"""
        prompt = f"""
        以下是若干文档章节的概要，请根据用户问题，选择最相关的章节标题。
        用户问题：{question}

        章节概要：
        {chr(10).join(f"{title}: {content}" for title, content in self.section_summaries.items())}

        请仅返回章节标题，不要输出解释。
        """

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )

        return response.choices[0].message.content.strip()

    def load_document(self, md_file_path: str) -> str:
        """加载Markdown文档并返回其内容"""
        if not md_file_path.endswith(".md"):
            md_file_path += ".md"

        if not os.path.exists(md_file_path):
            print(f"❌ 文档不存在: {md_file_path}")
            return ""

        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()

        except Exception as e:
            print(f"❗ 文档加载失败: {str(e)}")
            return ""

    def answer_question(self, document_content: str, question: str):
        """基于加载的文档和用户问题，直接回答问题"""
        prompt = f"""
        以下是文档的详细内容，请基于该文档回答用户的问题。回答要以正常语言叙述的方式呈现，简明扼要，不要生成其他结构。
        文档内容：
        {document_content}

        用户问题：
        {question}
        """

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )

        print(f"[助手]: {response.choices[0].message.content.strip()}\n")

if __name__ == "__main__":
    API_KEY = "sk-22146a806dcf42b68ab12ae2d4ddee7d"
    SUMMARY_FILE = "data/summary.md"
    MARKDOWN_FOLDER = "data/"

    ds_chat = DeepSeekChat(API_KEY)
    
    try:
        ds_chat.load_summary(SUMMARY_FILE)
        question = input("请输入您的问题：")
        
        start_time = time.time()
        # 获取相关章节
        relevant_section = ds_chat.get_relevant_section(question)
        clean_section = relevant_section.lstrip("# ").strip()
        print(f"✅ 选中的章节：{clean_section}")

        # 加载对应章节的文档
        markdown_path = os.path.join(MARKDOWN_FOLDER, clean_section)
        document_content = ds_chat.load_document(markdown_path)
        
        if document_content:
            # 直接回答用户问题
            ds_chat.answer_question(document_content, question)
            end_time = time.time()
            print(f"🕒 总用时：{end_time - start_time:.2f}秒")
        else:
            print("❗ 未找到相关章节内容，请检查路径或文件名。")
    except Exception as e:
        print(f"❌ 程序异常终止: {str(e)}")
