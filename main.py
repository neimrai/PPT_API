import os
from service.generate_presentation_outline import generate_presentation_outline
from service.standardize_outline_service import parse_outline_json
from service.generate_presentation_structure import generate_presentation_structure
from models.presentation_model import PresentationModel
import service.Layouts as Layouts
import random
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if __name__ == "__main__":
    
    prompt="纪念中国人民抗日战争暨世界反法西斯战争胜利80周年",
    n_slides=5,
    language="zh",
    # 1.创建PPT大纲
    outline = generate_presentation_outline(
      prompt=prompt,
      slide_number=n_slides,
      language=language
    )
    print("-----------------非格式化大纲-----------------")
    print(outline)
    # 2.格式化大纲
    outline_standardized = parse_outline_json(outline)
    print("-----------------格式化大纲-----------------")
    print(outline_standardized)
    if not outline_standardized:
        print("大纲格式化失败，无法继续生成PPT结构")
        exit(1)

    # 3.匹配模版
    layout = Layouts.get_layout_by_name("testcmy")
    layout_len = len(layout["slides"])
    # 4.生成PPT结构
    outline_structure = generate_presentation_structure(outline_standardized, layout)
    print("-------------PPT结构-----------------")
    print(outline_structure)


    # 5.创建演示文稿模型
    import uuid
    presentation_id = str(uuid.uuid4())
    
    presentation = PresentationModel(
        id=presentation_id,
        prompt=prompt,
        n_slides=n_slides,
        language=language,
        outlines=outline_standardized.model_dump(),
        layout=layout,
        structure=outline_structure,
    )
    # 6.生成图片

    image_generation_service = ImageGenerationService(os.getenv("PEXELS_API_KEY"))
    icon_finder_service = IconFinderService()
    async_asset_generation_tasks = []
    