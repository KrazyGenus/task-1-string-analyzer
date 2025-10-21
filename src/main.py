from fastapi import FastAPI, Request, HTTPException, status
from datetime import datetime, timezone
import httpx
from models.string_model import StringPayload
from utils.query_validator import get_validated_filters
from controllers.create_string import create_and_save_string, get_payload_by_id, delete_payload_by_id, get_by_query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
import json
import ast
app = FastAPI()


@app.get('/')
async def root():
    return {"root": "welcome to root!"}

@app.post('/strings', status_code=201)
async def create_string(payload: dict):
    try:
        data = StringPayload(**payload)
        StringPayload.validate_existence(data.value)
        response_payload = await create_and_save_string(data)
        return response_payload
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data type for "value" (must be string)'
        )

@app.get('/strings/{string_value}', status_code=200)
async def get_string(string_value:str):
    fetched_payload = await get_payload_by_id(string_value)
    if fetched_payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    return fetched_payload



@app.get('/strings')
async def query_string(is_palindrome, min_length, max_length, word_count, contains_character):
    if len(is_palindrome) == 0 or len(min_length) == 0  or len(max_length) == 0 or len(word_count) == 0 or len(contains_character) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query parameters"
        )
    
    str_json = f'{{"is_palindrome": {is_palindrome}, "min_length": {min_length}, "max_length": {max_length}, "word_count": {word_count}, "contains_character": "{contains_character}"}}'

    dict_json = json.loads(str_json)
    is_palindrome, min_length, max_length, word_count, contains_character = dict_json.values()
    get_validated_filters(is_palindrome, min_length, max_length, word_count, contains_character)
    query_results = await get_by_query(is_palindrome, min_length, max_length, word_count, contains_character)
    return query_results


@app.delete('/strings/{string_value}', status_code=204)
async def delete_string(string_value:str):
    fetched_payload = await delete_payload_by_id(string_value)
    if fetched_payload is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
