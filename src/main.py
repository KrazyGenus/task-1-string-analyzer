from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
import httpx
from models.string_model import StringPayload
from controllers.create_string import create_and_save_string
app = FastAPI()


@app.get('/')
async def root():
    return {"root": "welcome to root!"}

@app.post('/strings', status_code=201)
async def create_string(payload: StringPayload):
    response_payload = await create_and_save_string(payload)
    return response_payload