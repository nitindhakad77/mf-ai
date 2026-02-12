import os
import hashlib
import datetime
import cv2
from PIL import Image
import pytesseract
from mongo import get_collection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If Tesseract is NOT added to system PATH, keep this line
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Folder where images are stored
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_images")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def image_to_text(image_path: str) -> str:
    image = cv2.imread(image_path)

    if image is None:
        print(f"❌ Could not read image: {image_path}")
        return ""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    processed_image = Image.fromarray(thresh)

    text = pytesseract.image_to_string(processed_image)

    return text.strip()


def ingest_images():
    print("DB:", os.getenv("MONGO_URI"))
    col = get_collection()

    for fname in os.listdir(IMAGE_DIR):
        path = os.path.join(IMAGE_DIR, fname)

        if not os.path.isfile(path):
            continue

        # Only process images
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        print(f"Processing: {fname}")

        content = image_to_text(path)

        if not content:
            print("⚠ No text extracted")
            continue

        h = sha256(content)

        # Idempotency check
        if col.find_one({"content_hash": h}):
            print("⏭ Already exists in DB")
            continue

        doc = {
            "source": "image_ocr",
            "log_type": "image_extract",
            "filename": fname,
            "content": content,
            "content_hash": h,
            "ingested_at": datetime.datetime.utcnow(),
            "status": "raw",
        }

        col.insert_one(doc)
        print("✅ Inserted into DB")


if __name__ == "__main__":
    ingest_images()