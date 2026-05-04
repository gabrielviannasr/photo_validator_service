photo-validation-service/
│
├── app/
│   ├── main.py              # entrypoint da API
│   ├── routes/
│   │   └── validation.py    # endpoints
│   │
│   ├── services/
│   │   └── image_service.py # lógica de validação
│   │
│   ├── core/
│   │   └── config.py        # configs (env, constantes)
│   │
│   ├── models/
│   │   └── response_model.py # modelos de resposta
│   │
│   └── utils/
│       └── image_utils.py   # funções auxiliares (opcional)
│
├── tests/
│   └── test_validation.py
│
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
└── README.md


🐳 1. Rodando com Docker (usando seu Dockerfile)

Dentro da pasta photo-validation-service:

📦 Build da imagem
```
docker build -t photo-validation-service .
```

▶️ Rodar o container
```
docker run -p 8000:8000 photo-validation-service
```

🌐 Testar
```
http://localhost:8000/docs
```

🔥 2. Rodando sem Docker (só pra teste rápido)

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

✅ 1. Cria um ambiente virtual (evita quebrar o sistema)

Dentro do projeto:

```
python -m venv venv
```

✅ 2. Ativa o ambiente

No PowerShell:

```
.\venv\Scripts\activate
```

Se der erro de permissão:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
```

✅ 3. Atualiza o pip (importante)

```
python -m pip install --upgrade pip
```

✅ 4. Instala dependências

```
pip install -r requirements.txt
```

✅ 5. Rodar o projeto

```
python -m uvicorn app.main:app --reload
```