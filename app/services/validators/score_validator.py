from app.core.config import (
    MAX_SHARPNESS,
    IDEAL_BRIGHTNESS,
    MAX_BRIGHTNESS_DIFFERENCE,
    MAX_EYE_ALIGNMENT_DIFFERENCE,

    SHARPNESS_WEIGHT,
    BRIGHTNESS_WEIGHT,
    FACE_WEIGHT,

    CENTER_WEIGHT,
    FACE_SIZE_WEIGHT,
    HEAD_POSE_WEIGHT,

    CENTER_SCORE_NORMALIZER,
    IDEAL_FACE_RATIO,
    FACE_RATIO_NORMALIZER,

    MAX_NORMALIZED_SCORE
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
        min(
            sharpness / MAX_SHARPNESS,
            MAX_NORMALIZED_SCORE
        )
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
    center_distance = max(
        position_validation["centerDistanceX"],
        position_validation["centerDistanceY"]
    )

    center_score = (
        max(
            0,
            1 - (
                center_distance
                / CENTER_SCORE_NORMALIZER
            )
        )
        * CENTER_WEIGHT
    )

    score += center_score

    # --- tamanho do rosto ---
    ideal_face_ratio = IDEAL_FACE_RATIO

    face_ratio_difference = abs(
        position_validation["faceRatio"]
        - IDEAL_FACE_RATIO
    )

    face_size_score = (
        max(
            0,
            1 - (
                face_ratio_difference
                / FACE_RATIO_NORMALIZER
            )
        )
        * FACE_SIZE_WEIGHT
    )

    score += face_size_score

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
        * HEAD_POSE_WEIGHT
    )

    score += head_pose_score

    return {
        "validationScore": round(min(score, 1.0), 2),
        "sharpness_score": round(sharpness_score, 2),
        "brightness_score": round(brightness_score, 2),
        "center_score": round(center_score, 2),
        "face_size_score": round(face_size_score, 2),
        "head_pose_score": round(head_pose_score, 2)
    }