from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import shutil
import os
import json
from resume import parse_resume  # ✅ Correct (matches your file name)
 # Import your existing parser function

# Create FastAPI app
app = FastAPI(title="Resume Parser Web App", description="Upload resumes and extract details", version="1.0")

# Define upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve static files (Frontend HTML)
app.mount("/static", StaticFiles(directory="/Users/murthis/VScode/static"), name="static")


# 🔥 API Endpoint: Upload a Resume and Parse It
@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the resume using your existing function
    result = parse_resume(file_path)

    return {"filename": file.filename, "parsed_data": result}

# 🔥 API Endpoint: Serve Frontend (HTML Page)
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("static/index.html", "r") as file:
        return file.read()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)