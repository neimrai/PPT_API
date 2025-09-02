from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class StandardizedOutline:
    title: str
    slides: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    
class PresentationLayoutModel(BaseModel):
    name: str
    ordered: bool = Field(default=False)
    slides: List[StandardizedOutline]