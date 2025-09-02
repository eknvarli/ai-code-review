# AI Code Review API

Basit bir FastAPI uygulaması ile Python kodlarını otomatik olarak OpenAI GPT-3.5/4 modeli ile inceleyen bir API.

---

## Özellikler

- Python kodlarını arka planda değerlendirme.
- Kod hatalarını ve geliştirme önerilerini listeleme.
- SQLite veritabanı ile task yönetimi.
- Docker & Docker Compose desteği.

---

## Gereksinimler

- Python 3.12+
- pip
- Docker ve Docker Compose (opsiyonel, konteyner için)
- OpenAI API key

---

## Kurulum

1. Repo klonla:

```bash
git clone https://github.com/eknvarli/ai-code-review.git
cd ai-code-review
```

2. Sanal ortam oluştur ve aktif et:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Gerekli paketleri yükle:
```bash
pip install -r requirements.txt
```

4. OpenAI anahtarını main.py içerisindeki değişkene ekle.

## Çalıştırma

```bash
uvicorn main:app --reload
```

- API, varsayılan olarak http://127.0.0.1:8000 adresinde çalışır.

- Swagger dokümantasyonu: http://127.0.0.1:8000/docs

### Docker ile çalıştırma

1. Docker image oluştur:
```bash
docker build -t ai-code-review .
```

2. Docker container'ı başlat
```bash
docker run -p 8000:8000 --env OPENAI_API_KEY="sk-xxx" ai-code-review
```
veya Docker Compose kullan

```bash
docker-compose up --build
```

## API Endpoints

- **POST** `/tasks`
- Body örneği

```json
{
  "filename": "example.py",
  "content": "print('Hello world')"
}
```

- Dönen örnek

```json
{
  "id": 1,
  "filename": "example.py",
  "content": "print('Hello world')",
  "status": "pending",
  "report": null
}
```

**GET** `/tasks/{task_id}`

```json
{
  "id": 1,
  "filename": "example.py",
  "content": "print('Hello world')",
  "status": "success",
  "report": {
    "issues": [
      "Fonksiyon type hint eksik",
      "Hata yönetimi yapılmamış"
    ]
  }
}

```