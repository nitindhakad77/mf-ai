import cv2
import numpy as np
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def image_to_text_advanced(image_path: str) -> str:
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply threshold
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Convert back to PIL
    processed_image = Image.fromarray(thresh)

    return pytesseract.image_to_string(processed_image)

image_path="C:/Users/nitin/Pictures/Screenshots/nitin.png"
text = image_to_text_advanced(image_path)
print(text)