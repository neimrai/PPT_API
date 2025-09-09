import requests
import os
import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class ImageGenerationService:
    
    def __init__(self):
        self.api_url = os.getenv("IMAGE_URL")
        self.api_key = os.getenv("IMAGE_API_KEY")

    def get_image(self, prompt: str) -> str:
        response = requests.get(
            f"{self.api_url}?query={prompt}&per_page=1",
            headers={"Authorization": self.api_key},
        )
        data = response.json()
        print(data)
        # Check if the response contains any photos
        if not data.get("photos"):
            return "No image found"
        # 获取第一张图片的URL
        image_url = data["photos"][0]["src"]["large"]
        return image_url

if __name__ == "__main__":
    image_service = ImageGenerationService()
    image_url = image_service.get_image("beautiful landscape")
    print(image_url)