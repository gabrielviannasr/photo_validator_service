# ==========================================
# FACE POSITION VALIDATION
# ==========================================

# Tolerância para o rosto estar centralizado
FACE_CENTER_TOLERANCE_X = 0.15
FACE_CENTER_TOLERANCE_Y = 0.15

# Divisor usado no score contínuo de centralização
CENTER_SCORE_NORMALIZER = 0.30


# ==========================================
# FACE SIZE VALIDATION
# ==========================================

# Divisor usado no score contínuo de tamanho
FACE_RATIO_NORMALIZER = 0.50

# Faixa aceita para proporção do rosto
FACE_SIZE_MIN_RATIO = 0.50
FACE_SIZE_MAX_RATIO = 0.85

# Proporção ideal do rosto na imagem
IDEAL_FACE_RATIO = 0.65


# ==========================================
# IMAGE QUALITY
# ==========================================

IDEAL_BRIGHTNESS = 140
MAX_BRIGHTNESS_DIFFERENCE = 140
MAX_SHARPNESS = 500


# ==========================================
# HEAD POSE
# ==========================================

MAX_EYE_ALIGNMENT_DIFFERENCE = 0.05
MIN_EYE_OPENNESS = 0.015


# ==========================================
# SCORE WEIGHTS
# ==========================================

BRIGHTNESS_WEIGHT = 0.15
CENTER_WEIGHT = 0.10
EYES_VISIBLE_WEIGHT = 0.20
FACE_WEIGHT = 0.15
FACE_SIZE_WEIGHT = 0.05
HEAD_POSE_WEIGHT = 0.20
SHARPNESS_WEIGHT = 0.15


# ==========================================
# FINAL VALIDATION
# ==========================================

# Limite máximo usado na normalização contínua
MAX_NORMALIZED_SCORE = 1.0

# Nota mínima para aprovação da foto
VALIDATION_SCORE_THRESHOLD = 0.80