import json
from typing import Union, List
from datetime import datetime, time
from fastapi.responses import JSONResponse
import requests
from fastapi import FastAPI, Query, Path, HTTPException, Response
from typing_extensions import Annotated
from pydantic import BaseModel
from fastapi.responses import FileResponse
import io


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items2/")
async def read_items(q: Annotated[Union[str, None], Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.post("/text_to_image/")
async def text_to_image(text_prompt: str):
    data_dict = {"height": 512, "width": 512, "sampler": "K_DPM_2_ANCESTRAL", "text_prompts": [{"text": text_prompt, "weight": 1}]}
    response = requests.post(f'https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image', json=data_dict, headers={'Authorization': f'Bearer sk-2WbObPa0RGUhvah35Ii6BPvDLtTBUCnS8KxPGAZ3T1rBzDuQ'})

    assert len(response.content) > 0
    
    return Response(response.json()['artifacts'][0]['base64'], media_type="image/png")


