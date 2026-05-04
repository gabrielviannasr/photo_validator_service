import cv2
import numpy as np
import tempfile

async def analyze_image(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(await file.read())
        path = temp.name

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = np.mean(gray)

    return {
        "sharpness": float(sharpness),
        "brightness": float(brightness),
        "approved": bool(sharpness > 100 and brightness > 50)
    }