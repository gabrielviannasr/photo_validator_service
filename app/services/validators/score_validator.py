def calculate_validation_score(
    sharpness,
    brightness,
    face_validation,
    position_validation,
    head_pose_validation
):
    score = 0.0

    # --- nitidez ---
    if sharpness > 100:
        score += 0.20

    # --- brilho ---
    if brightness > 50:
        score += 0.15

    # --- rosto detectado ---
    if face_validation["faceDetected"]:
        score += 0.20

    # --- apenas um rosto ---
    if not face_validation["multipleFaces"]:
        score += 0.10

    # --- centralizado ---
    if position_validation["centered"]:
        score += 0.15

    # --- tamanho correto ---
    if position_validation["faceSizeOk"]:
        score += 0.10

    # --- cabeça reta ---
    if head_pose_validation["headStraight"]:
        score += 0.10

    return round(score, 2)