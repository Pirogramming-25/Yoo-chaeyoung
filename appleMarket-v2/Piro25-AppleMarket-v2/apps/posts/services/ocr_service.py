import os
import numpy as np
from PIL import Image, ImageEnhance

os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_enable_pir_api'] = '0'

from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='korean')

def extract_text_from_image(image_file):
    image = Image.open(image_file).convert('RGB')
    
    w, h = image.size
    image = image.resize((w * 2, h * 2), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    image_np = np.array(image)
    
    try:
        result = ocr.ocr(image_np, cls=False)
    except Exception:
        result = ocr.ocr(image_np)
    
    extracted_texts = []
    if result and result[0]:
        for line in result[0]:
            text = line[1][0]
            extracted_texts.append(text)
            
    return extracted_texts