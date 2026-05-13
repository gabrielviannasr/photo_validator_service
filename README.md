# Photo Validation Service

Microserviço de validação biométrica para fotos 3x4/documentais.

O serviço analisa automaticamente a qualidade da imagem e valida critérios biométricos para verificar se a foto é adequada para identificação em documentos, carteiras de benefício, cadastro ou autenticação.

---

# Funcionalidades

O serviço realiza validações automáticas de:

- Nitidez da imagem
- Brilho/iluminação
- Detecção facial
- Múltiplos rostos
- Centralização do rosto
- Proporção/tamanho do rosto
- Inclinação vertical da cabeça (roll)
- Rotação lateral da cabeça (yaw)
- Visibilidade dos olhos
- Detecção de landmarks faciais com MediaPipe
- Score contínuo de validação biométrica

---

# Tecnologias utilizadas

- Python 3.11
- FastAPI
- OpenCV
- MediaPipe
- Uvicorn
- Docker

---

# Estrutura do projeto

```text
photo-validation-service/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── core/
│   ├── models/
│   └── utils/
│
├── tests/
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

---

# Como funciona a validação

O sistema gera um score contínuo entre `0.0` e `1.0`.

A foto é aprovada quando:

```python
validationScore >= 0.80
```

Cada critério contribui com um peso específico no score final.

---

# Critérios avaliados

| Critério | Descrição |
|---|---|
| Sharpness | Verifica nitidez da imagem |
| Brightness | Avalia iluminação |
| Face Detection | Detecta presença facial |
| Multiple Faces | Reprova múltiplos rostos |
| Center Position | Verifica centralização |
| Face Size | Valida proporção do rosto |
| Head Pose | Detecta inclinação da cabeça |
| Eyes Visible | Verifica visibilidade dos olhos |
| Yaw Validation | Detecta rotação lateral |

---

# Configuração

As regras do sistema podem ser ajustadas em:

```text
app/core/config.py
```

---

# Principais configurações

## Centralização do rosto

```python
FACE_CENTER_TOLERANCE_X = 0.15
FACE_CENTER_TOLERANCE_Y = 0.15
```

Define a tolerância permitida para deslocamento do rosto.

---

## Tamanho do rosto

```python
FACE_SIZE_MIN_RATIO = 0.50
FACE_SIZE_MAX_RATIO = 0.85
```

Define a faixa aceitável da proporção do rosto em relação à imagem.

---

## Qualidade da imagem

```python
IDEAL_BRIGHTNESS = 140
MAX_SHARPNESS = 500
```

Define parâmetros ideais de iluminação e nitidez.

---

## Pose da cabeça

```python
MAX_EYE_ALIGNMENT_DIFFERENCE = 0.05
```

Define tolerância para inclinação da cabeça.

---

## Validação lateral (Yaw)

```python
YAW_DIFFERENCE_THRESHOLD = 0.04
```

Controla a tolerância de rotação lateral da cabeça.

---

## Threshold de aprovação

```python
VALIDATION_SCORE_THRESHOLD = 0.80
```

Nota mínima necessária para aprovação.

---

# Score weights

Os pesos abaixo definem a influência de cada critério no score final:

```python
BRIGHTNESS_WEIGHT = 0.10
CENTER_WEIGHT = 0.10
EYES_VISIBLE_WEIGHT = 0.15
FACE_WEIGHT = 0.15
FACE_SIZE_WEIGHT = 0.05
HEAD_POSE_WEIGHT = 0.20
SHARPNESS_WEIGHT = 0.15
YAW_WEIGHT = 0.10
```

---

# Exemplo de resposta

```json
{
  "analysis": {
    "eyeAlignmentDifference": 0.0023,
    "yawDifference": 0.0015
  },
  "face": {
    "centered": true,
    "faceDetected": true,
    "faceSizeOk": false,
    "landmarksDetected": true,
    "multipleFaces": false,
    "headStraight": true,
    "eyesVisible": true,
    "yawOk": true
  },
  "metrics": {
    "brightness": 204.81,
    "sharpness": 806.49
  },
  "score": {
    "brightnessScore": 0.05,
    "centerScore": 0.08,
    "faceSizeScore": 0.03,
    "eyeScore": 0.10,
    "headPoseScore": 0.19,
    "sharpnessScore": 0.15,
    "yawScore": 0.10
  },
  "validationScore": 0.85,
  "approved": true
}
```

---

# Rodando localmente

## Criar ambiente virtual

```bash
python -m venv venv
```

---

## Ativar ambiente virtual

### Windows PowerShell

```bash
.\venv\Scripts\activate
```

Se necessário:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
```

---

## Atualizar pip

```bash
python -m pip install --upgrade pip
```

ou

```bash
pip install --upgrade pip
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Validar ambiente

Verificar se as principais ferramentas foram instaladas corretamente:

```bash
python --version
pip --version
pytest --version
uvicorn --version
```

---

## Executar testes automatizados

```bash
pytest
```

---

## Executar projeto

```bash
python -m uvicorn app.main:app --reload
```

---

# Recriando o ambiente virtual

Caso existam problemas com dependências, cache ou ambiente virtual corrompido:

## Desativar ambiente virtual

```bash
deactivate
```

---

## Remover ambiente virtual

```powershell
Remove-Item -Recurse -Force venv
```

---

## Criar novo ambiente virtual

```bash
python -m venv venv
```

---

## Ativar ambiente virtual

```bash
.\venv\Scripts\activate
```

---

## Atualizar pip

```bash
python -m pip install --upgrade pip
```

---

## Instalar dependências novamente

```bash
pip install -r requirements.txt
```

---

## Executar testes

```bash
pytest
```

---

# Limpando cache do projeto

## Remover cache Python

```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

---

## Remover cache do pytest

```powershell
Remove-Item -Recurse -Force .pytest_cache
```