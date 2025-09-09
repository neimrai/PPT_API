from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
import uuid

@dataclass
class ImageAsset:
    """
    图片资源类，用于存储图片相关信息
    """
    path: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    extras: Optional[dict] = field(default=None)
