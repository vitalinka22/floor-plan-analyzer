import os
import tempfile # for creating temporary files that auto-delete

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from main import analyze # Import the analyze function from main.py

app = FastAPI(
    title = "Floor Plan Analyzer API", 
    description = "Analyzes German floor plan PDFs and extract property data", 
    version = "1.0.0"
)

@app.get("/health")
def health():
    return{"status" : "ok", "message" : "Floor Analyzer is runnig"}

@app.post("/analyze")
async def analyze_floor_plan(file: UploadFile = File(...)):

    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = analyze(tmp_path)
        return JSONResponse(content=result)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"error" : str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error" : str(e)})
    finally:
        os.remove(tmp_path)
