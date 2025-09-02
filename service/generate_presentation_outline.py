import os
import logging
from service.web_search_service import WebSearchService
from openai import OpenAI
import dotenv
import asyncio

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

#系统提示词
try:
    with open('prompts/system_outline_prompt.txt', 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    logger.debug("成功加载系统提示词")
except Exception as e:
    logger.error(f"加载系统提示词失败: {str(e)}")
    system_prompt = "请为用户生成一个PPT大纲。"

#用户提示词
def get_user_prompt(prompt: str, n_slides: int, language: str, content: str):
    logger.debug(f"生成用户提示词: 主题='{prompt}', 幻灯片数={n_slides}, 语言={language}")
    return f"""
        **Input:**
        - Prompt: {prompt}
        - Output Language: {language}
        - Number of Slides: {n_slides}
        - Additional Information: {content}
    """

def create_openai_client():
    logger.debug("创建OpenAI客户端")
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    return client

def generate_presentation_outline(prompt: str, slide_number=5, language="zh") -> str:
    logger.info(f"开始生成演示文稿大纲，主题: '{prompt}', 幻灯片数: {slide_number}, 语言: {language}")
    
    client = create_openai_client()
    
    #联网信息
    web_search_service = WebSearchService()
    logger.info("正在获取联网信息...")

    try:
        context = web_search_service.search(prompt)
        logger.info(f"联网信息获取成功，内容长度: {len(context)} 字符")
    except Exception as e:
        logger.error(f"获取联网信息失败: {str(e)}")
        context = "无法获取联网信息。"
    
    #消息列表
    messages = [
            {'role': 'system',
            'content': system_prompt},
            {'role': 'user',
            'content': get_user_prompt(prompt, slide_number, language, context)}
        ]
    logger.info("正在生成大纲...")
    
    try:
        completion = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        result = completion.choices[0].message.content
        logger.info("大纲生成成功✅")
        return result
    except Exception as e:
        logger.error(f"生成大纲时出错: {str(e)}")
        raise
