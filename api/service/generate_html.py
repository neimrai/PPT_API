import logging
from openai import OpenAI
import dotenv
import sys
import os
import re
import time
  
dotenv.load_dotenv()
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

  
# 读取HTML提示词文件
system_prompt = open("api\\prompts\\HTML-prompt2.md", 'r', encoding='utf-8').read()

# 用户提示词
def get_user_prompt(language, outline, response_schema=None):
    return f"""
## Slide Content Language
{language}

## Slide Outline
{outline}

## 输出要求
提供一个完整的、可独立运行的HTML代码。

幻灯片之间使用清晰的注释 <!-- SLIDE SPLIT --> 进行分隔。

代码需整洁、规范，符合标准。

最终成果应兼具 SlideShare 幻灯片的美观度 和 PowerPoint 般的专业结构与稳定性。
"""

def generate_slide_html(language, outline):
    logger.info("生成HTML内容...")
    logger.debug("创建OpenAI客户端")
    
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_BASE_URL"),
    )

    # 使用从文件中读取的系统提示词
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': get_user_prompt(language, outline)}
    ]
    
    logger.info("正在生成内容...")
    try:
        # 设置stream=True启用流式输出
        stream = client.chat.completions.create(
            model="deepseek-v3-241226",  
            messages=messages,
            stream=True,
            temperature=0.3,
            max_tokens=10000,
        )

        # 用于收集完整响应
        full_content = ""
        
        # 创建临时文件用于实时保存生成内容
        temp_output_file = "temp_html_output.txt"
        
        print("\n开始生成HTML内容...\n" + "-"*50)
        
        # 处理流式响应
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content_chunk = chunk.choices[0].delta.content
                full_content += content_chunk
                
                # 打印每个块的内容（不换行）
                print(content_chunk, end="", flush=True)
                
                # 将当前累积的内容写入临时文件
                with open(temp_output_file, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                    
        print("\n" + "-"*50 + "\n生成完成！")
        
        return full_content
    except Exception as e:
        logger.error(f"出错: {str(e)}")
        raise
      
def extract_and_save_html(content, output_filename):
    """从生成的内容中提取HTML并保存"""
    try:
        # 尝试匹配```html内容```
        match = re.search(r'```html\s*(.*?)\s*```', content, re.DOTALL)
        
        if match:
            html_content = match.group(1)
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n幻灯片内容已生成并保存到 {output_filename}")
            return True
        else:
            # 如果没有找到```html标记，检查是否整个内容就是HTML
            if content.strip().startswith('<!DOCTYPE html>') or content.strip().startswith('<html'):
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"\n幻灯片内容已生成并保存到 {output_filename}")
                return True
            else:
                logger.warning("未找到HTML内容，将保存原始输出")
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"\n原始内容已保存到 {output_filename}，但可能需要手动提取HTML部分")
                return False
    except Exception as e:
        logger.error(f"提取HTML内容出错: {str(e)}")
        return False

# if __name__ == "__main__":
#     logging.info("开始生成幻灯片内容...")
#     language = "zh"
    
#     # 获取输入文件路径，如果提供的话
#     input_file = "temp_files/temp_json/xuanyi.json"
#     if len(sys.argv) > 1:
#         input_file = sys.argv[1]
    
#     # 获取输出文件名，如果提供的话
#     output_file = "2025热门悬疑作品概述.html"
#     if len(sys.argv) > 2:
#         output_file = sys.argv[2]
    
#     # 读取大纲内容
#     try:
#         outline = open(input_file, 'r', encoding='utf-8').read()
#     except Exception as e:
#         logger.error(f"读取输入文件出错: {str(e)}")
#         sys.exit(1)
    
#     # 生成HTML内容（流式输出）
#     slide_content = generate_slide_html(language, outline)
    
#     # 提取并保存HTML内容
#     extract_and_save_html(slide_content, output_file)