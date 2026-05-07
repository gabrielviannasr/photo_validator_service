import cv2
import numpy as np
import tempfile
from app.core.config import (
    FACE_CENTER_TOLERANCE_X,
    FACE_CENTER_TOLERANCE_Y,
    FACE_SIZE_MIN_RATIO,
    FACE_SIZE_MAX_RATIO,
    VALIDATION_SCORE_THRESHOLD
)
from app.services.validators.face_landmarks_validator import (
    detect_face_landmarks
)
from app.services.validators.head_pose_validator import (
    validate_head_straight
)
from app.services.validators.score_validator import (
    calculate_validation_score
)

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

def validate_face_position_and_size(faces, image_shape):
    if len(faces) != 1:
        return {
            "centered": False,
            "faceSizeOk": False
        }

    (x, y, w, h) = faces[0]

    img_h, img_w = image_shape[:2]

    # --- centro do rosto ---
    face_center_x = x + w / 2
    face_center_y = y + h / 2

    img_center_x = img_w / 2
    img_center_y = img_h / 2

    # --- tolerância (15%) ---
    tolerance_x = img_w * FACE_CENTER_TOLERANCE_X
    tolerance_y = img_h * FACE_CENTER_TOLERANCE_Y

    centered = (
        abs(face_center_x - img_center_x) < tolerance_x and
        abs(face_center_y - img_center_y) < tolerance_y
    )

    # --- tamanho do rosto ---
    face_ratio = h / img_h
    face_size_ok = FACE_SIZE_MIN_RATIO <= face_ratio <= FACE_SIZE_MAX_RATIO

    return {
        "centerDistanceX": float(abs(face_center_x - img_center_x) / img_w),
        "centerDistanceY": float(abs(face_center_y - img_center_y) / img_h),
        "centered": bool(centered),
        "faceRatio": float(face_ratio),
        "faceSizeOk": bool(face_size_ok)
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
    
    # identifica pontos de referência facial (olhos, nariz, boca, etc.)
    landmarks = detect_face_landmarks(img)

    # valida se a cabeça está reta ou inclinada com base na posição dos olhos 
    head_pose_validation = validate_head_straight(landmarks)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- métricas atuais ---
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = np.mean(gray)

    # --- NOVO: detecção de rosto ---
    faces = detect_faces(gray)
    face_validation = validate_single_face(faces)

    position_validation = validate_face_position_and_size(faces, img.shape)

    validation_score = calculate_validation_score(
        sharpness,
        brightness,
        face_validation,
        position_validation,
        head_pose_validation
    )

    # approved = (
    #     sharpness > 100 and
    #     brightness > 50 and
    #     face_validation["faceDetected"] and
    #     not face_validation["multipleFaces"] and
    #     position_validation["centered"] and
    #     position_validation["faceSizeOk"] and
    #     head_pose_validation["headStraight"]
    # )

    approved = validation_score["validationScore"] >= VALIDATION_SCORE_THRESHOLD

    return {
        "landmarksDetected": landmarks is not None,
        "sharpness": float(sharpness),
        "brightness": float(brightness),
        "faceDetected": face_validation["faceDetected"],
        "multipleFaces": face_validation["multipleFaces"],
        "centered": bool(position_validation["centered"]),
        "faceSizeOk": bool(position_validation["faceSizeOk"]),
        "headStraight": head_pose_validation["headStraight"],
        "eyeAlignmentDifference": head_pose_validation["eyeAlignmentDifference"],
        "sharpnessScore": validation_score["sharpness_score"],
        "brightnessScore": validation_score["brightness_score"],
        "centerScore": validation_score["center_score"],
        "faceSizeScore": validation_score["face_size_score"],
        "headPoseScore": validation_score["head_pose_score"],
        "validationScore": validation_score["validationScore"],
        "approved": bool(approved)
    }