from datetime import datetime
from typing import List, Optional
from sqlalchemy import JSON, Column, DateTime
from sqlmodel import Field, SQLModel

from models.presentation_layout import PresentationLayoutModel
from models.presentation_outline_model import PresentationOutlineModel
from models.presentation_structure_model import PresentationStructureModel
from utils.randomizers import get_random_uuid


class PresentationModel(SQLModel, table=True):
    id: str = Field(primary_key=True)
    prompt: str
    n_slides: int
    language: str
    title: Optional[str] = None
    file_paths: Optional[List[str]] = Field(sa_column=Column(JSON), default=None)
    outlines: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.now))
    layout: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    structure: Optional[dict] = Field(sa_column=Column(JSON), default=None)

    def get_new_presentation(self):
        return PresentationModel(
            id=get_random_uuid(),
            prompt=self.prompt,
            n_slides=self.n_slides,
            language=self.language,
            title=self.title,
            file_paths=self.file_paths,
            outlines=self.outlines,
            layout=self.layout,
            structure=self.structure,
        )

    def get_presentation_outline(self):
        if not self.outlines:
            return None
        return PresentationOutlineModel(**self.outlines)

    def get_layout(self):
        return PresentationLayoutModel(**self.layout)

    def set_layout(self, layout: PresentationLayoutModel):
        self.layout = layout.model_dump()

    def get_structure(self):
        if not self.structure:
            return None
        return PresentationStructureModel(**self.structure)

    def set_structure(self, structure: PresentationStructureModel):
        self.structure = structure.model_dump()
