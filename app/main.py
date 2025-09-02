# main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from threading import Thread
import openai
import os

# -------------------------
# OpenAI API key
# -------------------------
openai.api_key = 'ENTER_YOUR_OPENAI_KEY'


# -------------------------
# Database setup
# -------------------------
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class CodeTask(Base):
    __tablename__ = "code_tasks"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(String, nullable=True)
    status = Column(String, default="pending")
    report = Column(JSON, nullable=True)


Base.metadata.create_all(bind=engine)

# -------------------------
# Pydantic schemas
# -------------------------
class CodeTaskCreate(BaseModel):
    filename: str
    content: str


class CodeTaskResponse(BaseModel):
    id: int
    filename: str
    content: str | None
    status: str
    report: dict | None

    class Config:
        orm_mode = True

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(title="AI Code Review API")


def run_task(task_id: int):
    db: Session = SessionLocal()
    task = db.query(CodeTask).filter(CodeTask.id == task_id).first()
    if not task:
        db.close()
        return

    try:
        task.status = "running"
        db.commit()

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful code reviewer."},
                {"role": "user", "content": f"Please review this Python code:\n{task.content}"}
            ]
        )

        issues_list = response.choices[0].message.content.split("\n")
        issues_list = [i.strip() for i in issues_list if i.strip()]
        task.report = {"issues": issues_list}
        task.status = "success"

    except Exception as e:
        task.status = "failed"
        task.report = {"error": str(e)}

    db.commit()
    db.close()


# -------------------------
# Endpoints
# -------------------------
@app.post("/tasks/", response_model=CodeTaskResponse)
def create_task(task: CodeTaskCreate):
    db = SessionLocal()
    db_task = CodeTask(filename=task.filename, content=task.content)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    db.close()

    Thread(target=run_task, args=(db_task.id,)).start()

    return db_task


@app.get("/tasks/{task_id}", response_model=CodeTaskResponse)
def get_task(task_id: int):
    db = SessionLocal()
    task = db.query(CodeTask).filter(CodeTask.id == task_id).first()
    db.close()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
