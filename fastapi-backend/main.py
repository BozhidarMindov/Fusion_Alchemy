import os
from uuid import uuid4

from fastapi import FastAPI
import uvicorn
import torch
from diffusers import StableDiffusionPipeline


app = FastAPI()

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
        # Save the image
        image.save(f"images/{uuid4()}.png")
        return {"message": "Avatar generated successfully"}
    except Exception as e:
        return {"message": "An error occurred while generating the avatar", "error": str(e)}


@app.get("/generate")
async def root(name: str):
    return generate_image(pipe, name)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
