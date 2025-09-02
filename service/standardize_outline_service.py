import dotenv
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

dotenv.load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class StandardizedOutline:
    title: str
    slides: List[Dict[str, Any]]
    metadata: Dict[str, Any]
def _standardize_outline(outline_data: Dict[str, Any]) -> StandardizedOutline:
    """标准化大纲格式"""
    # 提取基本信息
    title = outline_data.get("title", "")
    slides = outline_data.get("slides", [])
    metadata = outline_data.get("metadata", {})

    # 标准化slides
    standardized_slides = []
    for slide in slides:
        standardized_slide = {
            "page_number": slide.get("page_number", 0),
            "title": slide.get("title", ""),
            "content_points": slide.get("content_points", []),
            "slide_type": slide.get("slide_type", "content"),
            "description": slide.get("description", "")
        }
        
        # 只有当chart_config存在时才添加
        if "chart_config" in slide:
            standardized_slide["chart_config"] = slide["chart_config"]
            
        standardized_slides.append(standardized_slide)

    # 标准化metadata
    standard_metadata = {
        "language": metadata.get("language", "zh"),
        "total_slides": len(standardized_slides),
        "generated_with_ai": True
    }

    return StandardizedOutline(
        title=title,
        slides=standardized_slides,
        metadata=standard_metadata
    )

def _validate_outline(outline_data: Dict[str, Any]) -> bool:
    """验证大纲数据的完整性和正确性"""
    if not outline_data:
        return False

    if "title" not in outline_data or not outline_data["title"]:
        return False

    if "slides" not in outline_data or not isinstance(outline_data["slides"], list):
        return False

    for slide in outline_data["slides"]:
        if not isinstance(slide, dict):
            return False
        if "title" not in slide or not slide["title"]:
            return False

    return True

def parse_outline_json(ai_response: str) -> Optional[Dict[str, Any]]:
    """解析并标准化大纲JSON数据"""
    try:
        import json
        import re
        
        json_str = None
        # 方法1: 尝试提取```json```代码块中的内容
        json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', ai_response, re.DOTALL)
        if json_block_match:
            json_str = json_block_match.group(1)
            logger.info("从```json```代码块中提取大纲JSON")
        else:
            # 方法2: 尝试提取```代码块中的内容（不带json标识）
            code_block_match = re.search(r'```\s*(\{.*?\})\s*```', ai_response, re.DOTALL)
            if code_block_match:
                json_str = code_block_match.group(1)
                logger.info("从```代码块中提取大纲JSON")
            else:
                 # 方法3: 尝试提取完整的JSON对象
                  json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', ai_response, re.DOTALL)
                  if json_match:
                      json_str = json_match.group()
                      logger.info("使用正则表达式提取大纲JSON")
        if json_str:
            try:
                # 清理JSON字符串
                json_str = json_str.strip()
                json_str = re.sub(r',\s*}', '}', json_str)  # 移除}前的多余逗号
                json_str = re.sub(r',\s*]', ']', json_str)  # 移除]前的多余逗号

                json_data = json.loads(json_str)
                if _validate_outline(json_data):
                    # 标准化处理
                    standardized = _standardize_outline(json_data)
                    # 转换为字典并返回
                    return {
                        "title": standardized.title,
                        "slides": standardized.slides,
                        "metadata": standardized.metadata
                    }
                return None
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON: {e}")
                return None
    except Exception as e:
        logger.error(f"Error in parse_outline_json: {e}")
        return None
