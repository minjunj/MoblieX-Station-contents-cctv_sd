import base64
import os
import subprocess
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from rembg import remove

app = FastAPI()

async def save_upload_file(upload_file: UploadFile, destination_path: str):
    with open(destination_path, "wb") as buffer:
        data = await upload_file.read()
        buffer.write(data)

async def change_background(image_path):
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Command to change background
    cmd = f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}"

    try:
        subprocess.run(cmd, check=True, shell=True)
        print(f"Background changed to {image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to change background: {e}")

@app.get("/")
async def hello():
    print("hello")
    return "hello"

@app.post("/bg_change")
async def img2img(init_image: UploadFile = File(...)):
    image_path = "/app/out/uploaded_image.png"
    await save_upload_file(init_image, image_path)
    await change_background(image_path)
    return Response(content="Background changed", media_type="text/plain")
