from utils.string_factory import StringFactory
from models.string_model import StringPayload
from config.config import DB_INSTANCE_POOL

async def create_and_save_string(payload: StringPayload) -> dict:
    string_factory_instance = StringFactory(payload.value)
    stored_payload = string_factory_instance.create_response_payload()
    return stored_payload

async def get_payload_by_id(string_value:str)->dict | None:
    string_factory_instance = StringFactory(string_value)
    generated_hash = string_factory_instance.sha256_hash()
    found_payload = await DB_INSTANCE_POOL.retrieve_from_db(generated_hash)
    return found_payload


async def get_by_query(is_palindrome, min_length, max_length, word_count, contains_character):
    matching_payload = []
    ret_db = await DB_INSTANCE_POOL.get_all_db_content()
    
    # Iterate over the dictionaries (values) in the database result
    for doc in ret_db.values():
        properties = doc.get('properties', {})
        
        
        filters = [
           
            properties.get('is_palindrome') == is_palindrome, 
            
            
            properties.get('length', 0) >= min_length,
            properties.get('length', float('inf')) <= max_length, 

            properties.get('word_count', 0) == word_count,
            
           
            contains_character in properties.get('value', '') 
        ]
        
        
        if all(filters):
            matching_payload.append(doc)

    return matching_payload

async def delete_payload_by_id(string_value:str)-> bool:
    string_factory_instance = StringFactory(string_value)
    generated_hash = string_factory_instance.sha256_hash()
    payload_state = await DB_INSTANCE_POOL.delete_from_db(generated_hash)
    return payload_state