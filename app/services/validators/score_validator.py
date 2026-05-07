from app.core.config import (
    MAX_SHARPNESS,
    IDEAL_BRIGHTNESS,
    MAX_BRIGHTNESS_DIFFERENCE,
    MAX_EYE_ALIGNMENT_DIFFERENCE,

    SHARPNESS_WEIGHT,
    BRIGHTNESS_WEIGHT,
    FACE_WEIGHT
)


def calculate_validation_score(
    sharpness,
    brightness,
    face_validation,
    position_validation,
    head_pose_validation
):
    # --- penalidades críticas ---
    if not face_validation["faceDetected"]:
        return 0.0

    if face_validation["multipleFaces"]:
        return 0.0

    score = 0.0

    # --- nitidez contínua ---
    sharpness_score = (
        min(sharpness / MAX_SHARPNESS, 1.0)
        * SHARPNESS_WEIGHT
    )

    score += sharpness_score

    # --- brilho contínuo ---
    brightness_difference = abs(
        brightness - IDEAL_BRIGHTNESS
    )

    brightness_score = (
        max(
            0,
            1 - (
                brightness_difference
                / MAX_BRIGHTNESS_DIFFERENCE
            )
        )
        * BRIGHTNESS_WEIGHT
    )

    score += brightness_score

    # --- rosto detectado ---
    score += FACE_WEIGHT

    # --- centralização ---
    if position_validation["centered"]:
        score += 0.15

    # --- tamanho do rosto ---
    if position_validation["faceSizeOk"]:
        score += 0.10

    # --- alinhamento da cabeça contínuo ---
    eye_alignment_difference = (
        head_pose_validation["eyeAlignmentDifference"]
    )

    head_pose_score = (
        max(
            0,
            1 - (
                eye_alignment_difference
                / MAX_EYE_ALIGNMENT_DIFFERENCE
            )
        )
        * 0.10
    )

    score += head_pose_score

    return round(min(score, 1.0), 2)