# AI Code Review API

> If you want Turkish docs? [Click here](/docs/TR.md).

A simple FastAPI application that automatically reviews Python code using the OpenAI GPT-3.5/4 model.

---

## Features

- Evaluates Python code in the background.
- Lists code errors and improvement suggestions.
- Task management with SQLite database.
- Docker & Docker Compose support.

---

## Requirements

- Python 3.12+
- pip
- Docker and Docker Compose (optional, for containerization)
- OpenAI API key

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/eknvarli/ai-code-review.git
cd ai-code-review
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Add the OpenAI API key to the variable in `main.py`.

## Running the Application

```bash
uvicorn main:app --reload
```

- The API runs by default at http://127.0.0.1:8000.
- Swagger documentation: http://127.0.0.1:8000/docs

### Running with Docker

1. Build the Docker image:

```bash
docker build -t ai-code-review .
```

2. Start the Docker container:

```bash
docker run -p 8000:8000 --env OPENAI_API_KEY="sk-xxx" ai-code-review
```

Or use Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

- **POST** `/tasks`
- Request body example:

```json
{
  "filename": "example.py",
  "content": "print('Hello world')"
}
```

- Response example:

```json
{
  "id": 1,
  "filename": "example.py",
  "content": "print('Hello world')",
  "status": "pending",
  "report": null
}
```

- **GET** `/tasks/{task_id}`

```json
{
  "id": 1,
  "filename": "example.py",
  "content": "print('Hello world')",
  "status": "success",
  "report": {
    "issues": [
      "Missing type hints for functions",
      "No error handling implemented"
    ]
  }
}
```