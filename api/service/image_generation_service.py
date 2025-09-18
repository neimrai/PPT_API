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
        logging.info("图片生成服务已初始化")

    def get_image(self, prompt: str) -> str:
        logging.info(f"开始生成图片，使用提示词: '{prompt}'")
        response = requests.get(
            f"{self.api_url}?query={prompt}&per_page=1",
            headers={"Authorization": self.api_key},
        )
        # 处理响应
        if response.status_code != 200:
            logging.error(f"请求失败，状态码: {response.status_code}，响应: {response.text}")
            return "Request failed"
          
        data = response.json()
        # print(data)
        
        # Check if the response contains any photos
        if not data.get("photos"):
            logging.warning("未找到符合条件的图片。")
            return "No image found"
        # 获取第一张图片的URL
        image_url = data["photos"][0]["src"]["large"]
        logging.info(f"图片生成成功，图片URL: {image_url}")
        return image_url

# if __name__ == "__main__":
#     image_service = ImageGenerationService()
#     image_url = image_service.get_image("beautiful landscape")
#     print(image_url)