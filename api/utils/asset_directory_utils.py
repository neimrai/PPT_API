import os
import dotenv
dotenv.load_dotenv()

def get_images_directory():
    images_directory = os.path.join(os.getenv("APP_DATA_DIRECTORY"), "images")
    os.makedirs(images_directory, exist_ok=True)
    return images_directory


def get_exports_directory():
    export_directory = os.path.join(os.getenv("APP_DATA_DIRECTORY"), "exports")
    os.makedirs(export_directory, exist_ok=True)
    return export_directory

def get_uploads_directory():
    uploads_directory = os.path.join(os.getenv("APP_DATA_DIRECTORY"), "uploads")
    os.makedirs(uploads_directory, exist_ok=True)
    return uploads_directory
