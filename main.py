import os
from service.generate_presentation_outline import generate_presentation_outline
from service.standardize_outline_service import parse_outline_json

if __name__ == "__main__":

    
    # 创建PPT大纲
    outline = generate_presentation_outline(
      "深圳旅游旅游",
      slide_number=5,
      language="zh"
    )
    print("-----------------非格式化大纲-----------------")
    print(outline)
    # 格式化大纲
    outline_standardized = parse_outline_json(outline)
    print("-----------------格式化大纲-----------------")
    print(outline_standardized)
    # 生成html

    