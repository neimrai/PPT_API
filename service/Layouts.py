import logging
from typing import Dict, Any, List
from pathlib import Path
import json
import re
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def scan_builtin_layouts() -> List[Dict[str, Any]]:
    """扫描 presentation-templates 目录获取内置布局"""
    layouts_directory = Path("my-app/presentation-templates")

    # 确保目录存在
    if not layouts_directory.exists():
        logger.warning(f"布局目录不存在: {layouts_directory}")
        return []

    # 读取所有目录
    group_directories = [d for d in layouts_directory.iterdir() if d.is_dir()]
    logger.info(f"发现 {len(group_directories)} 个布局组")
      
    all_layouts = []
    for group_path in group_directories:
        
        group_name = group_path.name
        logger.info(f"正在扫描布局组: {group_name}")    
        # 扫描 .tsx 文件
        layout_files = [f for f in group_path.iterdir() 
                     if f.suffix == '.tsx' and not f.name.startswith('.')]
        logger.debug(f"在 {group_name} 中发现 {len(layout_files)} 个布局文件")
          
        # 读取 settings.json
        settings_path = group_path / 'settings.json'
        settings = None
        if settings_path.exists():
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                logger.debug(f"已加载布局组 {group_name} 的设置")
            except Exception as e:
                logger.error(f"加载布局组 {group_name} 的设置时出错: {str(e)}")
                settings = {
                    "description": f"{group_name} presentation layouts",
                    "ordered": False,
                    "default": False
                }
        else:
            logger.debug(f"布局组 {group_name} 没有设置文件，使用默认设置")
            settings = {
                "description": f"{group_name} presentation layouts",
                "ordered": False,
                "default": False
            }
          
        all_layouts.append({
            "groupName": group_name,
            "files": [f.name for f in layout_files],
            "settings": settings
        })
    logger.info(f"成功扫描 {len(all_layouts)} 个布局组")
    return all_layouts

def extract_schema_from_file(file_path: Path) -> Dict[str, Any]:
    """从文件中提取schema信息"""
    try:
        # 读取文件内容
        content = file_path.read_text(encoding='utf-8')
        logger.debug(f"正在从 {file_path} 提取模式信息")
        
        # 查找layoutDescription变量
        description_match = re.search(r'export\s+const\s+layoutDescription\s*=\s*"(.+?)"\s*;', content)
        description = description_match.group(1) if description_match else "A presentation slide"
        
        # 尝试解析Schema对象
        # 这是一个简化版本，实际实现可能需要更复杂的解析
        # 例如，可以寻找export const Schema = z.object({...})的模式
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"}
            }
        }

        # 尝试查找更多属性
        if "title" in content:
            schema["properties"]["title"] = {"type": "string"}
        if "subtitle" in content:
            schema["properties"]["subtitle"] = {"type": "string"}
        if "content" in content:
            schema["properties"]["content"] = {"type": "array"}
        if "items" in content:
            schema["properties"]["items"] = {"type": "array"}
        if "description" in content:
            schema["properties"]["description"] = {"type": "string"}
        
        logger.debug(f"从 {file_path.name} 提取的模式包含 {len(schema['properties'])} 个属性")
        return {
            "description": description,
            "json_schema": schema
        }
    except Exception as e:
        logger.error(f"从 {file_path} 提取模式时出错: {str(e)}")
        return {
            "description": "A presentation slide",
            "json_schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"}
                }
            }
        }

def get_layout_by_name(layout_name: str, session=None) -> Dict[str, Any]:
    """获取指定名称的布局"""
    logger.info(f"正在查找布局: {layout_name}")
    
    # 1. 扫描内置布局
    try:
        builtin_layouts = scan_builtin_layouts()
        logger.debug(f"扫描到 {len(builtin_layouts)} 个内置布局")
    except Exception as e:
        logger.error(f"扫描内置布局时出错: {str(e)}")
        builtin_layouts = []

    # 2. 查找匹配的布局组
    target_group = None
      
    # 首先在内置布局中查找
    for group in builtin_layouts:
        logger.debug(f"检查布局组: {group['groupName']}")
        if group["groupName"] == layout_name:
            logger.info(f"成功匹配布局组: {layout_name} ✅")
            target_group = group
            break
      
    # 如果没找到，在自定义布局中查找
    custom_layouts = []  # 这里需要实现自定义布局的获取逻辑
    if not target_group:
        logger.debug("在内置布局中未找到目标布局，尝试查找自定义布局")
        for group in custom_layouts:
            if group["groupName"] == layout_name:
                logger.info(f"在自定义布局中找到布局组: {layout_name}")
                target_group = group
                break
      
    if not target_group:
        logger.error(f"未找到布局组: {layout_name}")
        raise ValueError(f"Layout group '{layout_name}' not found")
      
    # 3. 构建返回的数据结构
    slides = []
    
    # 处理内置布局
    layouts_directory = Path("my-app/presentation-templates") / layout_name
    logger.debug(f"正在处理布局目录: {layouts_directory}")
    
    for file_name in target_group["files"]:
        file_path = layouts_directory / file_name
        logger.debug(f"处理布局文件: {file_path}")
        
        # 生成ID (去掉.tsx后缀)
        slide_id = file_name.replace('.tsx', '')
        
        # 使用正则表替换驼峰命名为空格分隔，作为name
        name = re.sub(r'([A-Z])', r' \1', slide_id).strip()
        
        # 提取schema和description
        schema_info = extract_schema_from_file(file_path)
        
        slides.append({
            "id": slide_id,
            "name": name,
            "description": schema_info["description"],
            "json_schema": schema_info["json_schema"]
        })
    
    logger.info(f"布局 {layout_name} 存在 {len(slides)} 个幻灯片")
    
    # 4. 返回符合预期格式的数据
    return {
        "name": layout_name,
        "ordered": target_group["settings"].get("ordered", False),
        "slides": slides
    }

# if __name__ == "__main__":
    # all_layouts = scan_builtin_layouts()
    # print(json.dumps(all_layouts, indent=2, ensure_ascii=False))
    # general_layout = get_layout_by_name("general")
    # print(general_layout.json())