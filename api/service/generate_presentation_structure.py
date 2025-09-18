import os
import dotenv
import json
import logging
import random
from openai import OpenAI
from typing import Dict, Any, List
# from Layouts import get_layout_by_name
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

# PPT结构设计prompt
def get_messages(layout: Dict[str, Any],n_layout:int, n_slides: int, outline_str: str) -> List[Dict[str, str]]:
    messages = [
            {'role': 'system',
            'content': f'''
              您是一位专业的演示设计师，拥有自由的创作空间来设计引人入胜的演示文稿。
              {json.dumps(layout, indent=2, ensure_ascii=False) }
              # 布局概述
              该布局包含 {n_layout} 种不同的幻灯片布局，每种布局都有独特的设计和结构。
              # 设计理念 
              - 创建视觉上引人注目且多样化的演示文稿 
              - 将布局与内容目的和受众需求相匹配 
              - 优先考虑参与度而不是严格的格式规则

              # 布局选择指南 
              1. **内容驱动的选择**：让幻灯片的目的指导布局选择 
                  - 开始/结束 → 标题布局 
                  - 流程/工作流程 → 可视化流程布局 
                  - 比较/对比 → 并排布局 
                  - 数据/指标 → 图表/图形布局 
                  - 概念/想法 → 图像 + 文本布局 
                  - 关键见解 → 重点布局
              2. **视觉多样性**：力求呈现多样化、引人入胜的演示流程 
                  - 自然地混合文本较多和视觉较多的幻灯片 
                  - 判断何时重复服务于内容 
                  - 平衡幻灯片间的信息密度
              3. **观众体验**：考虑幻灯片如何协同工作 
                  - 在主题之间创建自然的过渡 
                  - 使用增强理解的布局 
                  - 设计以实现最大影响力和留存率

              **相信你的设计直觉。专注于为内容和受众打造最有效的演示。**
              根据最能满足演示目标的方式为 {n_slides} 张幻灯片选择布局索引。用列表表示每个幻灯片对应的布局索引。
              若你需要表示第1张幻灯片使用布局索引0，第2张幻灯片使用布局索引2，第3张幻灯片使用布局索引1，第4张幻灯片使用布局索引3
              则输出列表[0, 2, 1, 3]

              # 🧾【输出格式要求】：请严格使用如下列表格式进行输出，
              [0, 2, 1, 3, 0, 1, 2, 0]

              '''},
            {'role': 'user',
            'content': outline_str}
        ]
    return messages

def create_openai_client():
    logger.debug("创建OpenAI客户端")
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_API_BASE_URL"),
    )
    return client

def generate_presentation_structure(outline: Dict[str, Any], layout: Dict[str, Any]) -> List[int]:
    logger.info(f"开始生成演示文稿结构，标题: '{outline['title']}', 幻灯片数: {len(outline['slides'])}")

    client = create_openai_client()
    
    # 准备消息列表
    messages = get_messages(layout,len(layout["slides"]), len(outline['slides']), outline.__str__())
    logger.debug(f"已准备提示信息，系统提示长度: {len(messages[0]['content'])}字符, 用户提示长度: {len(messages[1]['content'])}字符")
    
    logger.info("正在调用API生成PPT结构...")
    try:
        completion = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        result_text = completion.choices[0].message.content
        logger.info(f"API返回的原始文本结果: {result_text}")
         # 解析结果文本为列表
        try:
            # 首先尝试使用json.loads解析
            import re
            
            # 尝试提取列表部分
            match = re.search(r'\[\s*\d+(?:\s*,\s*\d+)*\s*\]', result_text)
            if match:
                list_str = match.group(0)
                result_list = json.loads(list_str)
                logger.info(f"成功解析为列表: {result_list}")
            else:
                # 如果无法提取列表，尝试提取所有数字
                numbers = re.findall(r'\d+', result_text)
                result_list = [int(num) for num in numbers]
                logger.info(f"从文本中提取的数字列表: {result_list}")
            
            # 确保列表长度与幻灯片数量一致
            slide_count = len(outline['slides'])
            if len(result_list) != slide_count:
                logger.warning(f"生成的列表长度 {len(result_list)} 与幻灯片数 {slide_count} 不匹配，进行调整")
                # 如果列表过短，生成随机索引
                if len(result_list) < slide_count:
                    last_item = random.randint(0, len(result_list) - 1)
                    result_list.extend([last_item] * (slide_count - len(result_list)))
                # 如果列表过长，截断
                if len(result_list) > slide_count:
                    result_list = result_list[:slide_count]
            
            return result_list
            
        except Exception as e:
            logger.error(f"解析API返回结果时出错: {str(e)}")
            # 生成默认列表
            default_list = [0] * len(outline['slides'])
            logger.warning(f"使用默认列表: {default_list}")
            return default_list
    except Exception as e:
        logger.error(f"生成PPT结构时出错: {str(e)}")
        raise

