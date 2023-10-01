import os
from uuid import uuid4

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

# Load the Stable Diffusion model
SDV5_MODEL_PATH = os.environ.get("SDV5_MODEL_PATH")
pipe = StableDiffusionPipeline.from_pretrained(SDV5_MODEL_PATH,
                                               torch_dtype=torch.float16)
pipe = pipe.to("cuda")


def generate_image(pipe, name):
    try:
        base_prompt = f"""
        In a future where avatars reflect personality,
        generate an avatar for {name}, a human explorer.
        Realistic, sense of awe, cool, futuristic, inspiring, beautiful, tech, cyber, clear face, no blur, cyberpunk
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
async def root(request_data: dict):
    name = request_data.get("name")
    return generate_image(pipe, name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
