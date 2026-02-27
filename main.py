from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst
from tools import read_financial_document
from task import create_analysis_task

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str):
    document_text = read_financial_document(file_path)

    task = create_analysis_task(document_text, query)

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )

    result = financial_crew.kickoff()
    return result


@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_financial_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document")
):

    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        response = run_crew(query=query, file_path=file_path)

        return {
            "status": "success",
            "analysis": response,
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)