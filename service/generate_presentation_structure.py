import os
import dotenv
from openai import OpenAI
from typing import Dict, Any, List


dotenv.load_dotenv()

def get_messages(layout: Dict[str, Any], n_slides: int, outline_str: str) -> List[Dict[str, str]]:
    messages = [
            {'role': 'system',
            'content': f'''
              您是一位专业的演示设计师，拥有自由的创作空间来设计引人入胜的演示文稿。
              {layout.to_string()}

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
              根据最能满足演示目标的方式为每张 {n_slides} 张幻灯片选择布局索引。'''},
            {'role': 'user',
            'content': outline_str}
        ]
    return messages

def create_openai_client():
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    return client

def generate_presentation_outline(outline: Dict[str, Any], layout: Dict[str, Any]) -> List[int]:
    client = create_openai_client()

    #消息列表
    messages = get_messages(layout, len(outline["slides"]), outline.to_string())
    completion = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )
    return completion.choices[0].message.content

        
if __name__ == "__main__":
   outline = '''{
  "title": "南澳岛旅游攻略：碧海蓝天与潮汕风情的完美融合",
  "total_pages": 5,
  "page_count_mode": "final",
  "slides": [
    {
      "page_number": 1,
      "title": "封面页",
      "content_points": [
        "南澳岛旅游攻略",
        "探索粤东海上明珠",
        "2025年最新玩法与贴士"
      ],
      "slide_type": "title",
      "type": "cover",
      "description": "以视觉冲击力强的封面吸引观众注意，展现南澳岛的自然美景与文化特色。",
      "chart_config": {}
    },
    {
      "page_number": 2,
      "title": "目录页",
      "content_points": [
        "十大必去景点",
        "八大高性价比餐厅",
        "交通与住宿指南",
        "特色玩法推荐",
        "避坑与实用建议"
      ],
      "slide_type": "content",
      "type": "menu",
      "description": "清晰展示PPT结构，帮助观众快速了解内容分布。",
      "chart_config": {}
    },
    {
      "page_number": 3,
      "title": "十大必去景点揭秘",
      "content_points": [
        "青澳湾：粤东最美沙滩",
        "环岛公路：自驾天堂",
        "三囱崖灯塔：浪漫地标",
        "大鹏山：登高望远",
        "金银岛：海盗传说"
      ],
      "slide_type": "content",
      "type": "points",
      "description": "介绍南澳岛核心景点，突出其自然与人文特色。",
      "chart_config": {
        "type": "bar",
        "data": {
          "labels": ["青澳湾", "环岛公路", "三囱崖灯塔", "大鹏山", "金银岛"],
          "datasets": [
            {
              "label": "游客评分（满分5分）",
              "data": [4.9, 4.7, 4.8, 4.6, 4.5],
              "backgroundColor": "#4ECDC4"
            }
          ]
        },
        "options": {
          "plugins": {
            "title": {
              "display": true,
              "text": "南澳岛十大景点游客评分"
            }
          }
        }
      }
    },
    {
      "page_number": 4,
      "title": "八大高性价比餐厅推荐",
      "content_points": [
        "阿来小炒：海鲜排档之王",
        "许大姐的菜：家常风味",
        "回归线咖啡：海边文艺",
        "成发牛肉火锅：潮汕盛宴",
        "然记糖水店：甜蜜记忆"
      ],
      "slide_type": "content",
      "type": "points",
      "description": "推荐本地特色餐厅，突出性价比与地道风味。",
      "chart_config": {
        "type": "pie",
        "data": {
          "labels": ["海鲜", "牛肉火锅", "甜品", "家常菜", "咖啡"],
          "datasets": [
            {
              "label": "美食偏好分布",
              "data": [40, 25, 15, 10, 10],
              "backgroundColor": ["#FF6B6B", "#4ECDC4", "#FFD93D", "#9467BD", "#E377C2"]
            }
          ]
        },
        "options": {
          "plugins": {
            "title": {
              "display": true,
              "text": "南澳岛美食类型偏好"
            }
          }
        }
      }
    },
    {
      "page_number": 5,
      "title": "交通住宿与避坑指南",
      "content_points": [
        "自驾技巧：限速与观景位",
        "轮渡提示：飞鱼伴航彩蛋",
        "住宿推荐：悬崖民宿与渔村",
        "避坑建议：海鲜陷阱与拍照雷区"
      ],
      "slide_type": "conclusion",
      "type": "summary",
      "description": "总结实用信息，帮助游客高效规划行程。",
      "chart_config": {
        "type": "radar",
        "data": {
          "labels": ["交通", "住宿", "饮食", "安全", "体验"],
          "datasets": [
            {
              "label": "旅行满意度评估",
              "data": [4.8, 4.7, 4.9, 4.6, 4.5],
              "borderColor": "#FF6B6B",
              "backgroundColor": "rgba(255, 107, 107, 0.2)"
            }
          ]
        },
        "options": {
          "plugins": {
            "title": {
              "display": true,
              "text": "南澳岛旅行满意度雷达图"
            }
          }
        }
      }
    }
  ],
  "metadata": {
    "scenario": "南澳岛旅游攻略展示，适用于自由行游客、旅游从业者、社交媒体内容创作者等。",
    "language": "zh",
    "total_slides": 5,
    "generated_with_ai": true,
    "enhanced_with_charts": true,
    "content_depth": "professional"
  }
}'''
   
   result = generate_presentation_outline(outline)
   print(result)