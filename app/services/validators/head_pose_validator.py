"""
O que esse código faz:
 - Compara a altura dos olhos para determinar se a cabeça está reta ou inclinada.
 - Se a diferença entre as alturas dos olhos for menor que uma tolerância definida, considera-se que a cabeça está reta.
"""

EYE_ALIGNMENT_TOLERANCE = 0.03

def validate_head_straight(landmarks):
    if landmarks is None:
        return {
            "headStraight": False
        }

    left_eye = landmarks.landmark[33]
    right_eye = landmarks.landmark[263]

    eye_y_difference = abs(left_eye.y - right_eye.y)

    head_straight = eye_y_difference < EYE_ALIGNMENT_TOLERANCE

    return {
        "headStraight": bool(head_straight),
        "eyeAlignmentDifference": float(eye_y_difference)
    }