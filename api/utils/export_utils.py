import json
import os
import requests  
import uuid
from typing import Literal
from fastapi import HTTPException
from pathvalidate import sanitize_filename

from api.models.pptx_models import PptxPresentationModel
from api.models.presentation_and_path import PresentationAndPath
from api.service.pptx_presentation_creator import PptxPresentationCreator
from api.service.temp_file_service import TempFileService

from api.utils.randomizers import get_random_uuid
from api.utils.asset_directory_utils import get_exports_directory


def export_presentation(  
    presentation_id: str, title: str, export_as: Literal["pptx", "pdf"]
) -> PresentationAndPath:
    if export_as == "pptx":
        # Get the converted PPTX model from the Next.js service
        try:
            response = requests.get(  # 同步请求
                f"http://localhost/api/presentation_to_pptx_model?id={presentation_id}"
            )
            if response.status_code != 200:  # status_code 而不是 status
                print(f"Failed to get PPTX model: {response.text}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to convert presentation to PPTX model",
                )
            pptx_model_data = response.json()  # 同步获取 JSON
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to connect to conversion service",
            )

        # Create PPTX file using the converted model
        pptx_model = PptxPresentationModel(**pptx_model_data)
        TEMP_FILE_SERVICE = TempFileService()
        temp_dir = TEMP_FILE_SERVICE.create_temp_dir()
        pptx_creator = PptxPresentationCreator(pptx_model, temp_dir)
        pptx_creator.create_ppt()  # 移除 await（假设这个方法也需要改为同步）

        export_directory = get_exports_directory()
        pptx_path = os.path.join(
            export_directory,
            f"{sanitize_filename(title or str(uuid.uuid4()))}.pptx",
        )
        pptx_creator.save(pptx_path)

        return PresentationAndPath(
            presentation_id=presentation_id,
            path=pptx_path,
        )
    else:
        try:
            response = requests.post(  # 同步 POST 请求
                "http://localhost/api/export-as-pdf",
                json={
                    "id": presentation_id,
                    "title": sanitize_filename(title or get_random_uuid()),
                },
            )
            response_json = response.json()  # 同步获取 JSON
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to connect to PDF export service",
            )

        return PresentationAndPath(
            presentation_id=presentation_id,
            path=response_json["path"],
        )