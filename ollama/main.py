from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import base64
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "testrigtesting"

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")  # FIXED this line



#     return render_template('index.html')
# return templates.TemplateResponse("index.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/upload-image/")
async def upload_image(prompt: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()

    # Convert image to base64
    image_base64 = base64.b64encode(contents).decode("utf-8")

    # Construct prompt — adjust this based on how your model expects the image
    full_prompt = f"{prompt}\n[image:base64]\n{image_base64}"

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        result = {"error": str(e)}

    return {
        "message": "Image uploaded and processed.",
        "filename": file.filename,
        "model_response": result
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

