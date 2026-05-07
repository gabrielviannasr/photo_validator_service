import math

from app.core.config import (
    MIN_EYE_OPENNESS
)

# landmarks principais dos olhos
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145

RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374


def calculate_distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )


def validate_eyes_visible(landmarks):
    if landmarks is None:
        return {
            "eyesVisible": False,
            "eyeOpennessScore": 0.0
        }

    # olho esquerdo
    left_top = landmarks.landmark[LEFT_EYE_TOP]
    left_bottom = landmarks.landmark[LEFT_EYE_BOTTOM]

    # olho direito
    right_top = landmarks.landmark[RIGHT_EYE_TOP]
    right_bottom = landmarks.landmark[RIGHT_EYE_BOTTOM]

    # abertura vertical
    left_eye_opening = calculate_distance(
        left_top,
        left_bottom
    )

    right_eye_opening = calculate_distance(
        right_top,
        right_bottom
    )

    average_eye_opening = (
        left_eye_opening + right_eye_opening
    ) / 2

    eyes_visible = average_eye_opening > MIN_EYE_OPENNESS

    return {
        "eyesVisible": bool(eyes_visible),
        "eyeOpennessScore": float(
            round(average_eye_opening, 4)
        )
    }