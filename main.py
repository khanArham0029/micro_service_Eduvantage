from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported"})

    try:
        contents = await file.read()
        doc = fitz.open(stream=contents, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return {
            "success": True,
            "text": full_text,
            "length": len(full_text)
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to extract PDF", "details": str(e)})
