from fastapi import FastAPI, Request, HTTPException, status
import httpx
from models.string_model import StringPayload
from utils.query_validator import get_validated_filters
from controllers.create_string import create_and_save_string, get_payload_by_id, delete_payload_by_id, get_by_query
from pydantic import ValidationError
import json

app = FastAPI()

###########################################################################################
# Creates a new string payload in the system.                                            #
# The function validates the input payload, ensuring it adheres to the required schema.  #
# If the payload is valid, it is saved in the system and returned.                       #
#                                                                                         #
# Args:                                                                                   #
#     payload (dict): The input data containing the string payload to be created.         #
#                                                                                         #
# Raises:                                                                                 #
#     HTTPException: If the input payload is invalid, raises a 422 error.                #
#                                                                                         #
# Returns:                                                                                #
#     Dict: The created string payload.                                                   #
###########################################################################################
@app.post('/strings', status_code=201)
async def create_string(payload: dict):
    try:
        # Validate the input payload against the StringPayload model
        data = StringPayload(**payload)
        # Ensure the string value does not already exist in the system
        StringPayload.validate_existence(data.value)
        # Save the validated payload and return the response
        response_payload = await create_and_save_string(data)
        return response_payload
    except ValidationError:
        # Raise an error if the input payload is invalid
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data type for "value" (must be string)'
        )


###########################################################################################
# Retrieves a string payload from the system based on the provided string value.          #
# The function attempts to locate the payload using the given string value and returns    #
# it if found. If the string does not exist, an HTTP 404 exception is raised.             #
#                                                                                         #
# Args:                                                                                   #
#     string_value (str): The string value to identify the payload to be retrieved.       #
#                                                                                         #
# Raises:                                                                                 #
#     HTTPException: If the string does not exist in the system, raises a 404 error.      #
#                                                                                         #
# Returns:                                                                                #
#     Dict: The payload associated with the provided string value.                        #
###########################################################################################
@app.get('/strings/{string_value}', status_code=200)
async def get_string(string_value: str):
    fetched_payload = await get_payload_by_id(string_value)
    if fetched_payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    return fetched_payload



@app.get('/strings')
###########################################################################################
# Queries strings based on various filters such as palindrome status, length, word count, #
# and character containment.                                                              #
# Args:                                                                                   #
#    is_palindrome (str): Indicates if the string should be a palindrome ("true"/"false").#
#    min_length (str): The minimum length of the string.                                  #
#    max_length (str): The maximum length of the string.                                  #
#    word_count (str): The number of words the string should contain.                     #
#    contains_character (str): A specific character that the string must contain.         #
# Raises:                                                                                 #
#     HTTPException: If any of the query parameters are empty or invalid.                 #
# Returns:                                                                                #
#     List[Dict]: A list of dictionaries containing the query results.                    #
###########################################################################################
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
###########################################################################################
# Deletes a string payload from the system based on the provided string value.            #
# The function attempts to locate the payload using the given string value and deletes    #
# it if found. If the string does not exist, an HTTP 404 exception is raised.             #
#                                                                                         #
# Args:                                                                                   #
#     string_value (str): The string value to identify the payload to be deleted.         #
#                                                                                         #
# Raises:                                                                                 #
#     HTTPException: If the string does not exist in the system, raises a 404 error.      #
###########################################################################################
async def delete_string(string_value:str):
    fetched_payload = await delete_payload_by_id(string_value)
    if fetched_payload is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
