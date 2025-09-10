import os
import asyncio
import json
from api.service.generate_presentation_outline import generate_presentation_outline
from api.service.standardize_outline_service import parse_outline_json
from api.service.generate_presentation_structure import generate_presentation_structure
from api.service.image_generation_service import ImageGenerationService
from api.service.icon_finder_service import IconFinderService
from api.service.generate_slide_content import generate_slide_content
from api.utils.process_slides import process_slide_and_fetch_assets
from api.utils.export_utils import export_presentation
import api.service.Layouts as Layouts
from typing import Dict, Any, List, Optional


from api.models.presentation_model import PresentationModel
from api.models.slides import SlideModel
import random
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if __name__ == "__main__":
    
    prompt="Ai绘图模型Nano Banana",
    n_slides=3,
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
    print("-------------选择的布局-----------------")
    layout = Layouts.get_layout_by_name("test")
    print(layout)
    layout_len = len(layout["slides"])
    
    # 4.生成PPT结构
    print("-------------PPT结构-----------------")
    outline_structure = generate_presentation_structure(outline_standardized, layout)
    print(outline_structure)


    # 5.创建演示文稿模型
    import uuid
    presentation_id = str(uuid.uuid4())
    
    presentation = PresentationModel(
        id=presentation_id,
        prompt=prompt,
        n_slides=n_slides,
        language=language,
        outlines=outline_standardized,
        layout=layout,
        structure=outline_structure,
    )
    # 6.集成图片生成和图标搜索功能
    print("-------------集成图片生成和图标搜索功能-----------------")
    image_generation_service = ImageGenerationService()
    icon_finder_service = IconFinderService()
    async_asset_generation_tasks = []
    
    # 7.根据幻灯片布局和大纲生成结构化内容
    slides: List[SlideModel] = []          # 存储所有幻灯片模型
    slide_contents: List[dict] = []        # 存储所有幻灯片内容
    for i, slide_layout_index in enumerate(outline_structure):
        # 单页幻灯片布局
        slide_layout = layout["slides"][slide_layout_index] if slide_layout_index < layout_len else None
        print(f"第{i+1}页幻灯片选择的布局: {slide_layout}")
        # 根据布局和大纲生成幻灯片内容
        slide_content = generate_slide_content(
          slide_layout=slide_layout,
          language=language,
          outline=outline_standardized["slides"][i] if i < len(outline_standardized) else None
        )
        print(f"第{i+1}页幻灯片内容: {slide_content}")
        # 将 JSON 字符串解析为字典
        slide_content = json.loads(slide_content) if isinstance(slide_content, str) else slide_content
        
        slide = SlideModel(
            id=presentation_id,
            layout_group=layout["name"] if layout else None, # 布局名称
            layout=slide_layout["id"] if slide_layout else None, # 布局ID
            index=i,
            speaker_notes=slide_content.get("__speaker_note__",""), # 演讲者注释
            content=slide_content
        )
        # 添加到列表
        slides.append(slide)
        slide_contents.append(slide_content)
        
        # 添加异步任务
        task = process_slide_and_fetch_assets(
            image_generation_service,
            icon_finder_service,
            slide
        )
        async_asset_generation_tasks.append(task)
 

    # 8. 执行异步任务

    async def run_async_tasks():
        try:
            generated_assets_lists = await asyncio.gather(*async_asset_generation_tasks)
            generated_assets = []
            for assets_list in generated_assets_lists:
                if assets_list:  # 确保 assets_list 不为 None
                    generated_assets.extend(assets_list)
            return generated_assets
        except Exception as e:
            print(f"执行异步任务时出错: {str(e)}")
            return []

    # 运行异步任务
    if async_asset_generation_tasks:
        generated_assets = asyncio.run(run_async_tasks())
    else:
        generated_assets = []


    # 9. 导出演示文稿
    try:
        # 确保有标题
        presentation_title = outline_standardized.get("title", "Untitled Presentation")
        # 导出演示文稿
        presentation_result = export_presentation(
            presentation_id=presentation_id,
            title=presentation_title,
            format_type="pptx"
        )
        # 打印结果
        if presentation_result:
            result = {
                "presentation_id": presentation_id,
                "title": presentation_title,
                "file_path": presentation_result.file_path if hasattr(presentation_result, 'file_path') else None,
                "edit_path": f"/presentation?id={presentation_id}"
            }
            print("演示文稿导出成功:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("演示文稿导出失败")
            
    except Exception as e:
        print(f"导出演示文稿时出错: {str(e)}") 