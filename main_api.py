from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from src.handler import run_text, run_pdf
import logging

app = FastAPI()

def run_text(query_text: str):
    logging.info(f"Query User: {query_text}")
    return f"Processed text: {query_text}"

def run_file(file: UploadFile):
    logging.info(f"File uploaded: {file.filename}")
    return f"Processed file: {file.filename}"

@app.post("/process_text/")
async def process_text(text: str = Form(...)):
    response = run_text(text)
    return JSONResponse(content={"response": response})

@app.post("/process_file/")
async def process_file(file: UploadFile):
    response = run_file(file)
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1111)
