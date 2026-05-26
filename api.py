from fastapi import FastAPI

app = FastAPI(
    title = "Floor Plan Analyzer API", 
    description = "Analyzes German floor plan PDFs and extract property data", 
    version = "1.0.0"
)

@app.get("/health")
def health():
    return{"status" : "ok", "message" : "Floor Analyzer is runnig"}