from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()


model_id = "stabilityai/stable-diffusion-2-1"
device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = StableDiffusionPipeline.from_pretrained(model_id).to(device)

class LogoRequest(BaseModel):
    prompt: str
    negative_prompt: str
    width: int
    height: int
    seed: int | None

@app.post("/generate_logo")
async def generate_logo(request: LogoRequest):
    try:
        generator = torch.Generator(device).manual_seed(request.seed) if request.seed else None
        image = pipeline(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=50,
            guidance_scale=7.5,
            generator=generator
        ).images[0]
        
       
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {"image": image_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



