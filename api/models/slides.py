from dataclasses import dataclass
from typing import Optional

@dataclass
class SlideModel:
    id: str
    layout_group: str
    layout: int
    index: int
    speaker_notes: Optional[str]
    content: dict