import os
from service.web_search_service import WebSearchService
from openai import OpenAI
import dotenv
import asyncio

dotenv.load_dotenv()

#系统提示词
with open('prompts\system_outline_prompt.txt', 'r', encoding='utf-8') as file:
    system_prompt = file.read()

#用户提示词
def get_user_prompt(prompt: str, n_slides: int, language: str, content: str):
    return f"""
        **Input:**
        - Prompt: {prompt}
        - Output Language: {language}
        - Number of Slides: {n_slides}
        - Additional Information: {content}
    """


def create_openai_client():
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    return client

def generate_presentation_outline(prompt: str, slide_number=5, language="zh"):
    client = create_openai_client()
    #联网信息
    web_search_service = WebSearchService()

    context = web_search_service.search(prompt)
    #消息列表
    messages = [
            {'role': 'system',
            'content': system_prompt},
            {'role': 'user',
            'content': get_user_prompt(prompt, 5, "zh", context)}
        ]
    completion = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content







