import cv2
import base64
import requests
import numpy as np
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes
import os

class IMGnPDF_Preprocessor:
    def __init__(self, path_or_url):
        self.path_or_url = path_or_url
        self.original = None
        self.processed = None

    def download(self):
        if os.path.exists(self.path_or_url):
            if self.path_or_url.lower().endswith(".pdf"):
                pil_image = convert_from_bytes(open(self.path_or_url, "rb").read(), fmt='jpeg')[0].convert("RGB")
            else:
                pil_image = Image.open(self.path_or_url).convert("RGB")
        else:
            response = requests.get(self.path_or_url, timeout=10)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            content_bytes = BytesIO(response.content)
            if "application/pdf" in content_type or self.path_or_url.lower().endswith(".pdf"):
                pil_image = convert_from_bytes(content_bytes.read(), fmt='jpeg')[0].convert("RGB")
            else:
                pil_image = Image.open(content_bytes).convert("RGB")

        self.original = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        self.processed = self.original.copy()
        return self

    def to_grayscale(self):
        self.processed = cv2.cvtColor(self.processed, cv2.COLOR_BGR2GRAY)
        return self

    def adjust_contrast(self, contrast=1.5, brightness=0):
        self.processed = cv2.convertScaleAbs(self.processed, alpha=contrast, beta=brightness)
        return self

    def remove_background(self):
        self.processed = cv2.adaptiveThreshold(
            self.processed, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        return self

    def crop_largest_contour(self):
        contours, _ = cv2.findContours(self.processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            self.processed = self.processed[y:y+h, x:x+w]
        return self

    def get(self):
        return self.processed

    def get_base64(self, format='PNG'):
        if len(self.processed.shape) == 2:
            rgb_image = cv2.cvtColor(self.processed, cv2.COLOR_GRAY2RGB)
        else:
            rgb_image = cv2.cvtColor(self.processed, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(rgb_image)
        buffer = BytesIO()
        pil_image.save(buffer, format=format)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64


# Example usage: 
# preprocessor = IMGnPDF_Preprocessor("local_image.png")
# processed_b64 = preprocessor.download().to_grayscale().adjust_contrast().remove_background().get_base64()
