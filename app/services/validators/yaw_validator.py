# landmarks importantes
from app.core.config import YAW_DIFFERENCE_THRESHOLD

LEFT_EYE = 33
RIGHT_EYE = 263
NOSE_TIP = 1


def validate_face_yaw(landmarks):
    if landmarks is None:
        return {
            "yawOk": False,
            "yawScore": 0.0,
            "yawDifference": 1.0
        }

    left_eye = landmarks.landmark[LEFT_EYE]
    right_eye = landmarks.landmark[RIGHT_EYE]
    nose = landmarks.landmark[NOSE_TIP]

    # distâncias horizontais
    left_distance = abs(nose.x - left_eye.x)
    right_distance = abs(right_eye.x - nose.x)

    # diferença proporcional
    yaw_difference = abs(
        left_distance - right_distance
    )

    yaw_ok = yaw_difference < YAW_DIFFERENCE_THRESHOLD

    yaw_score = max(
        0,
        1 - (yaw_difference / YAW_DIFFERENCE_THRESHOLD)
    )

    return {
        "yawOk": bool(yaw_ok),
        "yawScore": round(yaw_score, 2),
        "yawDifference": float(
            round(yaw_difference, 4)
        )
    }