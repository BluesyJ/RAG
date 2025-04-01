import re
import os

def split_markdown_by_heading(file_path, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取Markdown文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式匹配大标题（如 "# 六、合同管理审批流程"）
    sections = re.split(r'(?=\n#\s*[一二三四五六七八九十]+、.*)', content)

    # 写入每个章节
    for i, section in enumerate(sections):
        if section.strip():  # 忽略空内容
            # 获取标题作为文件名
            title_match = re.match(r'#\s*([一二三四五六七八九十]+、.*?)\n', section)
            if title_match:
                title = title_match.group(1).strip().replace(' ', '_')
            else:
                title = f'未命名章节_{i}'

            output_path = os.path.join(output_dir, f'{title}.md')
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(section.strip())

    print(f'已成功将Markdown文件拆分为 {len(sections)} 个部分，并保存在 "{output_dir}" 目录下。')

# 示例用法
split_markdown_by_heading('output.md', 'output')
