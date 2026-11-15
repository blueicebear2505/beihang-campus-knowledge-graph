from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import csv

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Load and process map
original = Image.open("hangzhoubeihang.jpg")

image = original.resize(
    (original.width * 2, original.height * 2)
)

image = image.convert("L")
image = ImageEnhance.Contrast(image).enhance(2)
image = image.filter(ImageFilter.SHARPEN)

# Detect text
results = pytesseract.image_to_data(
    image,
    config="--psm 11",
    output_type=pytesseract.Output.DICT
)

candidates = []

for i, text in enumerate(results["text"]):

    code = text.strip().upper().replace(" ", "")

    if re.fullmatch(r"[CDRSLA]\d{1,2}", code):

        confidence = float(results["conf"][i])

        if confidence > 20:

            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]

            x_percent = (x + w / 2) / image.width * 100
            y_percent = (y + h / 2) / image.height * 100

            candidates.append({
                "map_code": code,
                "x": round(x_percent, 2),
                "y": round(y_percent, 2),
                "confidence": round(confidence, 1)
            })

# Save candidates separately
with open(
    "ocr_candidates.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "map_code",
            "x",
            "y",
            "confidence"
        ]
    )

    writer.writeheader()
    writer.writerows(candidates)

print(f"Saved {len(candidates)} detections.")
print("File: ocr_candidates.csv")
