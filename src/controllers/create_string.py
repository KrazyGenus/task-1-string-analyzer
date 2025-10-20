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

async def delete_payload_by_id(string_value:str)-> bool:
    string_factory_instance = StringFactory(string_value)
    generated_hash = string_factory_instance.sha256_hash()
    payload_state = await DB_INSTANCE_POOL.delete_from_db(generated_hash)
    return payload_state