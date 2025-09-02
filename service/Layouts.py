from typing import Dict, Any, List
from pathlib import Path
import json
import re
from dataclasses import dataclass

@dataclass
class PresentationLayoutModel:
    """演示文稿布局模型"""
    slides: List[Dict[str, Any]]
    ordered: bool
    description: str = ""
    default: bool = False
def scan_builtin_layouts() -> List[Dict[str, Any]]:
    """扫描 presentation-templates 目录获取内置布局"""
    layouts_directory = Path("presentation-templates")
      
    # 确保目录存在
    if not layouts_directory.exists():
        return []

    # 读取所有目录
    group_directories = [d for d in layouts_directory.iterdir() if d.is_dir()]
      
    all_layouts = []
    for group_path in group_directories:
        
        group_name = group_path.name
        print(f"Scanning layout group: {group_name}")    
        # 扫描 .tsx 文件
        layout_files = [f for f in group_path.iterdir() 
                     if f.suffix == '.tsx' and not f.name.startswith('.')]
          
        # 读取 settings.json
        settings_path = group_path / 'settings.json'
        settings = None
        if settings_path.exists():
            with open(settings_path, 'r') as f:
                settings = json.load(f)
        else:
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
    return all_layouts

def extract_schema_from_code(layout_code: str) -> Dict[str, Any]:
    """从布局代码中提取schema信息"""
    # 这里需要实现具体的schema提取逻辑
    # 临时返回空字典
    return {}
  
def get_layout_by_name(layout_name: str, session=None) -> PresentationLayoutModel:
    """获取指定名称的布局"""
    # 1. 扫描内置布局
    builtin_layouts = scan_builtin_layouts()

    # 2. 查找匹配的布局组
    target_group = None
      
    # 首先在内置布局中查找
    for group in builtin_layouts:
        if group["groupName"] == layout_name:
            target_group = group
            break
      
    # 如果没找到，在自定义布局中查找
    custom_layouts = []  # 这里需要实现自定义布局的获取逻辑
    if not target_group:
        for group in custom_layouts:
            if group["groupName"] == layout_name:
                target_group = group
                break
      
    if not target_group:
        raise ValueError(f"Layout group '{layout_name}' not found")
      
    # 4. 构建 PresentationLayoutModel
    slides = []
      
    if "layouts" in target_group:  # 自定义布局
        for layout in target_group["layouts"]:
            slides.append({
                "id": layout.layout_id,
                "name": layout.layout_name,
                "json_schema": extract_schema_from_code(layout.layout_code)
            })
    else:  # 内置布局
        for file_name in target_group["files"]:
            # 使用正则表替换驼峰命名为空格分隔
            name = re.sub(r'([A-Z])', r' \1', file_name.replace('.tsx', '')).strip()
            slides.append({
                "id": file_name.replace('.tsx', ''),
                "name": name,
                "json_schema": {}  # 需要从模块中提取
            })
      
    return PresentationLayoutModel(
        slides=slides,
        ordered=target_group["settings"]["ordered"],
        description=target_group["settings"].get("description", ""),
        default=target_group["settings"].get("default", False)
    )
    
if __name__ == "__main__":
    all_layouts = scan_builtin_layouts()
    print(json.dumps(all_layouts, indent=2, ensure_ascii=False))
