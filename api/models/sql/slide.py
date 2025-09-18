from typing import Optional
from sqlmodel import Field, Column, JSON, SQLModel

from utils.randomizers import get_random_uuid


class SlideModel(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=get_random_uuid)
    presentation: str
    layout_group: str
    layout: str
    index: int
    content: dict = Field(sa_column=Column(JSON))
    html_content: Optional[str]
    speaker_note: Optional[str]
    properties: Optional[dict] = Field(sa_column=Column(JSON))

    def get_new_slide(self, presentation_id: str, content: Optional[dict] = None):
        return SlideModel(
            id=get_random_uuid(),
            presentation=presentation_id,
            layout_group=self.layout_group,
            layout=self.layout,
            index=self.index,
            speaker_note=self.speaker_note,
            content=content or self.content,
            properties=self.properties,
        )
