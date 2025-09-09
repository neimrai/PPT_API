import logging
from openai import OpenAI
import dotenv
import os
from api.utils.schema import remove_fields_from_schema, add_field_in_schema

dotenv.load_dotenv()
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 系统提示词
system_prompt = """
Generate structured slide based on provided outline, follow mentioned steps and notes and provide structured output.

    # Steps
    1. Analyze the outline.
    2. Generate structured slide based on the outline.
    3. Generate speaker note that is simple, clear, concise and to the point.

    # Notes
    - Slide body should not use words like "This slide", "This presentation".
    - Rephrase the slide body to make it flow naturally.
    - Provide prompt to generate image on "__image_prompt__" property.
    - Provide query to search icon on "__icon_query__" property.
    - Only use markdown to highlight important points.
    - Make sure to follow language guidelines.
    - Speaker note should be normal text, not markdown.
    **Strictly follow the max and min character limit for every property in the slide.**
"""
#系统中文提示词
system_prompt_zh = """
根据提供的大纲生成结构化幻灯片，遵循提到的步骤和注意事项，并提供结构化输出。

    # 步骤
    1. 分析大纲。
    2. 根据大纲生成结构化幻灯片。
    3. 生成简单、清晰、简明扼要的演讲者备注。

    # 注意事项
    - 幻灯片正文不应使用“本幻灯片”、“本演示文稿”等词语。
    - 重新措辞幻灯片正文，使其自然流畅。
    - 在“__image_prompt__”属性上提供生成图像的提示。
    - 在“__icon_query__”属性上提供搜索图标的查询。
    - 仅使用markdown突出显示重要点。
    - 确保遵循语言指南。
    - 演讲者备注应为普通文本，而不是markdown。
    **严格遵循幻灯片每个属性的最大和最小字符限制。**
"""
# 用户提示词
def get_user_prompt(language, outline):
  return f"""
 ## Icon Query And Image Prompt Language
        English

        ## Slide Content Language
        {language}

        ## Slide Outline
        {outline}
  """
def create_openai_client():
    logger.debug("创建OpenAI客户端")
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    return client

def generate_slide_content(slide_layout,language, outline):
  logger.info("开始生成幻灯片内容")
  client = create_openai_client()
  
  #消息列表
  messages = [
          {'role': 'system',
          'content': system_prompt},
          {'role': 'user',
          'content': get_user_prompt(language, outline)}
      ]
  logger.info("正在生成幻灯片内容...")
  print("幻灯片布局:")
  print(slide_layout)
  response_schema = remove_fields_from_schema(
        slide_layout["json_schema"], ["__image_url__", "__icon_url__"]
    )
  print("移除__image_url__后的schema:")
  print(response_schema)
  
  response_schema = add_field_in_schema(
        response_schema,
        {
            "__speaker_note__": {
                "type": "string",
                "minLength": 100,
                "maxLength": 250,
                "description": "Speaker note for the slide",
            }
        },
        True,
    )
  print("添加__speaker_note__后的schema:")
  print(response_schema)
  try:
      completion = client.chat.completions.create(
          model=os.getenv("MODEL"),
          messages=messages,
          response_format=(
                {
                    "type": "json_schema",
                    "json_schema": response_schema
                }
            )
          )
      result = completion.choices[0].message.content
      logger.info("生成幻灯片内容成功✅")
      return result
  except Exception as e:
      logger.error(f"生成幻灯片内容时出错: {str(e)}")
      raise
