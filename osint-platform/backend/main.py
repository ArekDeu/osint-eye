from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from modules.name_search import search_by_name
from modules.email_search import search_by_email
from modules.phone_search import search_by_phone
from modules.image_search import search_by_image

app = FastAPI(title="OSINT Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def root():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "OSINT Platform API is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/search/name")
async def name_search(first_name: str = Form(...), last_name: str = Form(...)):
    results = await search_by_name(first_name, last_name)
    return {"status": "ok", "query": f"{first_name} {last_name}", "results": results}

@app.post("/api/search/email")
async def email_search(email: str = Form(...)):
    results = await search_by_email(email)
    return {"status": "ok", "query": email, "results": results}

@app.post("/api/search/phone")
async def phone_search(phone: str = Form(...)):
    results = await search_by_phone(phone)
    return {"status": "ok", "query": phone, "results": results}

@app.post("/api/search/image")
async def image_search(file: UploadFile = File(...)):
    image_data = await file.read()
    results = await search_by_image(image_data, file.filename)
    return {"status": "ok", "query": file.filename, "results": results}

@app.post("/api/search/all")
async def search_all(
    first_name: str = Form(default=""),
    last_name: str = Form(default=""),
    email: str = Form(default=""),
    phone: str = Form(default=""),
):
    results = {}
    if first_name and last_name:
        results["name"] = await search_by_name(first_name, last_name)
    if email:
        results["email"] = await search_by_email(email)
    if phone:
        results["phone"] = await search_by_phone(phone)
    return {"status": "ok", "results": results}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
