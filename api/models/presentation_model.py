from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class PresentationModel:
    id: str
    prompt: str
    n_slides: int
    language: str
    outlines: Dict[str, Any]
    layout: Dict[str, Any]
    structure: List[int]