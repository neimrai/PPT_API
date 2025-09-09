# -*- coding: utf-8 -*-
# coding:utf-8
import base64
import hashlib
import hmac
import random
import string
from datetime import datetime
import time
import requests
import uuid
import json
import dotenv
import os  # 添加 os 导入


class WebSearchService:
    """
    Web search service using Yayi API
    """

    def __init__(self):
        dotenv.load_dotenv()  # 移到初始化方法中
        self.base_url = 'https://yayi.wenge.com/saas-gateway/2deaeebb6f90aadd97ba018ce37465c4/analysis'
        self.url_path = '/2deaeebb6f90aadd97ba018ce37465c4/analysis'
        # 获取环境变量
        self.app_key = os.getenv("YAYI_APP_KEY")
        self.app_secret = os.getenv("YAYI_APP_SECRET_ENV")
        if not self.app_key or not self.app_secret:
            raise ValueError("YAYI_APP_KEY or YAYI_APP_SECRET_ENV environment variables are not set")


    def search(self, message: str):
        """
        Perform web search using Yayi API

        Args:
            message: The search query

        Returns:
            The search results from Yayi API
        """
        try:
            print(f"Request - Performing web search for: {message}")
            response = self.yayi_entirety_info(message)
            return response
        except Exception as e:
            print(f"Error performing web search: {e}")
            return {"error": str(e)}

    def yayi_entirety_info(self, message: str):
        """
        Yayi web search implementation

        Args:
            message: The search query

        Returns:
            The search results
        """
        date = self.get_current_time_gmt_format()
        content_type = 'application/json'
        accept = '*/*'
        method = 'POST'

        signature_str = self.generate_signature(
            method=method,
            accept=accept,
            content_type=content_type,
            date=date,
            url_path=self.url_path
        )

        data = {
            "id": self.generate_uuid_str(),
            "content": {
                "function": "web_QA",
                "prompt_max_tokens": 1800,
                "user_message": message,
                "web_source_list": ["quark"],
                "get_news_num": 10,
                "top_k": 5
            }
        }

        print(f"Request parameters: {data}")
        headers = self.generate_header(
            content_type=content_type,
            accept=accept,
            date=date,
            signature=signature_str
        )

        # Use io to run the request in a separate thread
        response = requests.post(self.base_url, json=data, headers=headers).json()

        res_info = response["data"]["res_info"]
        all_contexts = [v["context"] for v in res_info.values()]
        all_contexts = "\n".join(all_contexts)

        return all_contexts

    def generate_signature(self, method, accept, content_type, date, url_path):
        """
        Generate signature for API request

        Args:
            method: HTTP method
            accept: Accept header
            content_type: Content-Type header
            date: Date header
            url_path: URL path

        Returns:
            The generated signature
        """
        string_to_sign = method + "\n" + accept + "\n" + content_type + "\n" + date + "\n" + url_path
        string_to_sign = string_to_sign.encode('utf-8')
        secret_key = self.app_secret.encode('utf-8')  # 使用实例变量
        signature = hmac.new(secret_key, string_to_sign, hashlib.sha256).digest()
        return self.encode_base64_string(signature)

    def generate_header(self, content_type, accept, date, signature):
        """
        Generate request headers

        Args:
            content_type: Content-Type header
            accept: Accept header
            date: Date header
            signature: Signature

        Returns:
            The generated headers
        """
        headers = {
            'x-tilake-app-key': self.app_key,  
            'x-tilake-ca-signature-method': "",
            'x-tilake-ca-timestamp': self.get_current_timestamp(),
            'x-tilake-ca-nonce': self.generate_random_string(),
            'x-tilake-ca-signature': signature,
            'Date': date,
            'Content-Type': content_type,
            'Accept': accept}

        return headers

    def generate_random_string(self, length=16):
        """
        Generate random string

        Args:
            length: Length of random string, default is 16

        Returns:
            The generated random string
        """
        letters = string.ascii_letters + string.digits
        rand_str = ''.join(random.choice(letters) for i in range(length))
        return rand_str

    def get_current_time(self, format='%Y-%m-%d %H:%M:%S'):
        """
        Get current time

        Args:
            format: Time format, default is '%Y-%m-%d %H:%M:%S'

        Returns:
            Current time string
        """
        now = datetime.now()
        time_str = now.strftime(format)
        return time_str

    def get_current_timestamp(self):
        """
        Get current timestamp

        Returns:
            Current timestamp as string
        """
        timestamp_str = int(round(time.time() * 1000))
        return str(timestamp_str)

    def encode_base64_string(self, s):
        """
        Encode string with Base64

        Args:
            s: String to encode

        Returns:
            Encoded string
        """
        encoded = base64.b64encode(s).decode()
        return encoded

    def generate_uuid_str(self):
        """
        Generate UUID string

        Returns:
            UUID string without hyphens
        """
        uid = str(uuid.uuid4())
        uuid_str = ''.join(uid.split('-'))
        return uuid_str

    def get_current_time_gmt_format(self):
        """
        Get current time in GMT format

        Returns:
            Current time in GMT format
        """
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%SGMT+00:00'
        now = datetime.now()
        time_str = now.strftime(GMT_FORMAT)
        return time_str
