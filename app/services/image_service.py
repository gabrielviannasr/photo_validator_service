import cv2
import numpy as np
import tempfile

def detect_faces(gray_image):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.3,
        minNeighbors=5
    )

    return faces


def validate_single_face(faces):
    face_detected = len(faces) >= 1
    multiple_faces = len(faces) > 1

    return {
        "faceDetected": bool(face_detected),
        "multipleFaces": bool(multiple_faces)
    }


async def analyze_image(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(await file.read())
        path = temp.name

    img = cv2.imread(path)

    if img is None:
        return {
            "error": "Invalid image file"
        }

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- métricas atuais ---
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = np.mean(gray)

    # --- NOVO: detecção de rosto ---
    faces = detect_faces(gray)
    face_validation = validate_single_face(faces)

    approved = (
        sharpness > 100 and
        brightness > 50 and
        face_validation["faceDetected"] and
        not face_validation["multipleFaces"]
    )

    return {
        "sharpness": float(sharpness),
        "brightness": float(brightness),
        "faceDetected": face_validation["faceDetected"],
        "multipleFaces": face_validation["multipleFaces"],
        "approved": bool(approved)
    }