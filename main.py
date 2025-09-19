import os
import asyncio
import json
import logging
from api.service.generate_presentation_outline import generate_presentation_outline
from api.service.standardize_outline_service import parse_outline_json
from api.service.generate_presentation_structure import generate_presentation_structure
from api.service.image_generation_service import ImageGenerationService
from api.service.icon_finder_service import IconFinderService
from api.service.generate_slide_content import generate_slide_content
from api.service.generate_html import generate_slide_html, extract_and_save_html
from api.utils.process_slides import process_slide_and_fetch_assets
from api.utils.asset_directory_utils import get_exports_directory

import api.service.Layouts as Layouts
from typing import Dict, Any, List, Optional


from api.models.presentation_model import PresentationModel
from api.models.slides import SlideModel
from api.models.pptx_models import PptxPresentationModel

import random
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
if __name__ == "__main__":
    
    prompt="2025年热门悬疑作品概述"
    n_slides=10
    language="zh"
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
        slide_layout = layout["slides"][slide_layout_index]
        print(f"第{i+1}页幻灯片选择的布局: {slide_layout}")
        # 根据布局和大纲生成幻灯片内容
        slide_content = generate_slide_content(
          slide_layout=slide_layout,
          language=language,
          outline=outline_standardized["slides"][i]
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
        async_asset_generation_tasks.append(
            process_slide_and_fetch_assets(
                image_generation_service,
                icon_finder_service,
                slide
            )
        )

    # 8. 执行异步任务，获取资源URL
    async def run_async_tasks():
        try:
            generated_assets_lists = await asyncio.gather(*async_asset_generation_tasks)
            generated_assets = []
            for assets_list in generated_assets_lists:
                if assets_list:  # 确保 assets_list 不为 None
                    generated_assets.extend(assets_list)
            logging.info(f"所有异步任务完成，共生成 {len(generated_assets)} 个资源")
            return generated_assets
        except Exception as e:
            logging.error(f"执行异步任务时出错: {str(e)}")
            return []
    print("-------------幻灯片内容-----------------")
    print(slide_contents)

    asyncio.run(run_async_tasks())
    print("-------------幻灯片内容-----------------")
    print(slide_contents)
    print("-------------幻灯片模型-----------------")
    print(slides)
    # 9.内容组合导出HTML文件
    
    # 确保data文件夹存在
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"创建了 {data_dir} 文件夹")
        
    # 生成HTML内容（流式输出）
    slide_html = generate_slide_html(language, slides)
    
    # 提取并保存HTML内容
    html_file_path = os.path.join(data_dir, "test.html")
    extract_and_save_html(slide_html, html_file_path)
    print(f"HTML文件已保存到: {html_file_path}")
    
