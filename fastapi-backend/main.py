import codecs
import os
from uuid import uuid4

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch
from diffusers import StableDiffusionPipeline
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Define the directory to store generated images
image_directory = "images"

# Create a directory to store images if it doesn't exist
os.makedirs(image_directory, exist_ok=True)

app.mount("/images", StaticFiles(directory=image_directory), name="images")


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_config(config_file):
    with codecs.open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4",
                                               revision="fp16",
                                               torch_dtype=torch.float16,
                                               use_auth_token=parse_config("config.yaml")["huggingface_key"])

if torch.cuda.is_available():
    pipe = pipe.to("cuda")
else:
    pipe = pipe.to("cpu")


def generate_image(pipe, name):
    try:
        base_prompt = f"""
        An avatar for {name}, a human explorer.
        Realistic, sense of awe, cool, futuristic, inspiring, beautiful, tech, cyber, clear face, no blur, cyberpunk,
        Resilient, Determined, Mysterious, Enigmatic, Courageous, Weathered, Battle-scarred, Tenacious, Wise,
        Charismatic, Heroic, Thoughtful
        """
        # Generate an image based on the provided prompt
        image = pipe(base_prompt).images[0]
        image_path = os.path.join(image_directory, str(uuid4()) + ".png")
        image.save(image_path)

        return {"message": "Avatar generated successfully",
                "path": f"http://localhost:8000/{image_path}"}
    except Exception as e:
        return {"message": "An error occurred while generating the avatar", "error": str(e)}


@app.post("/generate")
async def generate_avatar(request_data: dict):
    name = request_data.get("name")
    return generate_image(pipe, name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
