import logging
from openai import OpenAI
import dotenv
import sys
import os
import re

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

## Output Format
You must strictly follow the provided JSON Schema format. Any deviation from the schema will be considered invalid.

## Steps
1. Analyze the outline.
2. Generate structured slide based on the outline.
3. Generate speaker note that is simple, clear, concise, and to the point.

## Notes
- Slide body should not use words like "This slide", "This presentation".
- Rephrase the slide body to make it flow naturally.
- Provide prompt to generate image on "__image_prompt__" property.
- Provide query to search icon on "__icon_query__" property.
- Only use markdown to highlight important points.
- Make sure to follow language guidelines.
- Speaker note should be normal text, not markdown.
**Strictly follow the max and min character limit for every property in the slide.**
"""

# 用户提示词
def get_user_prompt(language, outline,response_schema=None):
  return f"""
 Icon Query And Image Prompt Language: English

## Slide Content Language
{language}

## Slide Outline
{outline}

## Output Requirements
You must generate a complete JSON object that strictly follows the specified schema. 
Include all required fields with appropriate content based on the slide outline and language. 
Ensure the JSON output is valid and properly formatted.
  """

def generate_slide_content(slide_layout,language, outline):
  logger.info("开始生成幻灯片内容")
  logger.debug("创建OpenAI客户端")
  
  client = OpenAI(
        # api_key="613da2af-73af-4601-b8c4-8e3aa0246db2",
        # base_url="https://ark.cn-beijing.volces.com/api/v3",
        
        # api_key="sk-ea8d61bdf4d94d6cb3ff6803dbeca6f4",
        # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_BASE_URL"),
    )
  
  
  print("幻灯片布局:")
  print(slide_layout)
  
  
  response_schema = remove_fields_from_schema(
        slide_layout["json_schema"], ["__image_url__", "__icon_url__"]
    )
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
  print("响应的JSON Schema:")
  print(response_schema)
  
  
  #消息列表
  messages = [
          {'role': 'system',
          'content': system_prompt},
          {'role': 'user',
          'content': get_user_prompt(language, outline, response_schema)}
      ]
  logger.info("正在生成幻灯片内容...")
  try:
      completion = client.chat.completions.create(
          model = "deepseek-v3-241226",  # your model endpoint ID
          messages = [
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": get_user_prompt(language, outline, response_schema)},
          ],
          response_format={"type": "json_schema",
                          "json_schema": {
                            "name":"slide_content",
                            "schema":response_schema}},
          temperature=0.7,
          max_tokens=2000
      )

      result = completion.choices[0].message.content
      logger.info("生成幻灯片内容成功✅")
      json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', result, re.DOTALL)
      if json_block_match:
          json_str = json_block_match.group(1)
          logger.info("从```json```代码块中提取幻灯片内容JSON")
          logger.debug(f"模型返回的内容: {json_str}")
          return json_str

      logger.debug(f"模型返回的内容: {result}")
      return result
  except Exception as e:
      logger.error(f"生成幻灯片内容时出错: {str(e)}")
      raise

# if __name__ == "__main__":
#   slide_layout = '''{
#       "id": "about-company-slide",
#       "name": "About Our Company Slide",
#       "description": "A slide layout providing an overview of the company, its background, and key information.",
#       "json_schema": {
#         "$schema": "https://json-schema.org/draft/2020-12/schema",
#         "type": "object",
#         "properties": {
#           "title": {
#             "description": "Main title of the slide",
#             "type": "string",
#             "minLength": 3,
#             "maxLength": 30
#           },
#           "content": {
#             "description": "Main content text describing the company or topic",
#             "type": "string",
#             "minLength": 25,
#             "maxLength": 400
#           },
#           "companyName": {
#             "description": "Company name displayed in header",
#             "type": "string",
#             "minLength": 2,
#             "maxLength": 50
#           },
#           "date": {
#             "description": "Today Date displayed in header",
#             "type": "string",
#             "minLength": 5,
#             "maxLength": 30
#           },
#           "image": {
#             "description": "Optional supporting image for the slide (building, office, etc.)",
#             "type": "object",
#             "properties": {
#               "__image_url__": {
#                 "description": "URL to image",
#                 "type": "string",
#                 "format": "uri"
#               },
#               "__image_prompt__": {
#                 "type": "string",
#                 "minLength": 10,
#                 "maxLength": 50
#               }
#             },
#             "required": ["__image_url__", "__image_prompt__"],
#             "additionalProperties": false
#           }
#         },
#         "required": ["title", "content", "companyName", "date"],
#         "additionalProperties": false
#       }
#     }'''
#   language="zh"
#   outline = {'title': '钩织艺术的基础知识', 'slides': [{'page_number': 1, 'title': '封面页', 'content_points': ['钩织艺术的基础知识', '从零开始掌握钩针编织', '探索针法与符号的奥秘'], 'slide_type': 'title', 'description': '吸引观众注意力，展示主题与整体风格', 'chart_config': {}}, {'page_number': 2, 'title': '目录页', 'content_points': ['钩针基础符号', '基础针法详解', '线材与钩针选择', '练习建议与结语'], 'slide_type': 'content', 'description': '引导观众了解PPT内容结构', 'chart_config': {}}, {'page_number': 3, 'title': '钩针基础符号', 'content_points': ['CH=锁针', 'X=短针', 'V=短针加针', 'A=短针减针', 'Sl=引拔针'], 'slide_type': 'content', 'description': '介绍钩针图解中常见的基础符号及其含义', 'chart_config': {'type': 'table', 'data': {'columns': ['符号', '中文名称', '英文缩写', '图解特征'], 'rows': [['CH', '锁针', 'ch', '圆圈图案'], ['X', '短针', 'sc/dc', '三角底竖线'], ['V', '加针', 'inc', '两针入一针出'], ['A', '减针', 'dec', '三针并一针'], ['Sl', '引拔针', 'sl st', '小圆点']]}, 'options': {'responsive': True}}}, {'page_number': 4, 'title': '基础针法详解', 'content_points': ['短针（X）', '中长针（T）', '长针（F）', '引拔针（Sl）', '特殊针法（W/M）'], 'slide_type': 'content', 'description': '深入讲解钩针的五种核心针法及操作要点', 'chart_config': {'type': 'bar', 'data': {'labels': ['短针', '中长针', '长针', '引拔针', '特殊针法'], 'datasets': [{'label': '高度比例', 'data': [1, 2, 3, 0, 1], 'backgroundColor': '#4ECDC4'}]}, 'options': {'responsive': True, 'plugins': {'legend': {'display': False}, 'title': {'display': True, 'text': '针法高度对比'}}, 'scales': {'y': {'beginAtZero': True}}}}}, {'page_number': 5, 'title': '练习建议与结语', 'content_points': ['选择合适线材', '初学者推荐钩针', '观看视频教程', '练习基础针法', '欢迎交流反馈'], 'slide_type': 'conclusion', 'description': '提供实用建议并鼓励观众实践与交流', 'chart_config': {'type': 'radar', 'data': {'labels': ['易用性', '性价比', '美观度', '耐用性', '学习价值'], 'datasets': [{'label': '钩织材料评分', 'data': [9, 8, 7, 8, 9], 'borderColor': '#FF6B6B', 'backgroundColor': 'rgba(255, 107, 107, 0.2)'}]}, 'options': {'responsive': True, 'plugins': {'legend': {'display': False}}}}}], 'metadata': {'language': 'zh', 'total_slides': 5, 'generated_with_ai': True}}
#   import json
#   slide_layout = json.loads(slide_layout)
#   slide_content = generate_slide_content(slide_layout ,language, outline["slides"][1].__str__())
#   print("生成的幻灯片内容:")
#   print(slide_content)
  