from utils.string_factory import StringFactory
from models.string_model import StringPayload

async def create_and_save_string(payload: StringPayload) -> dict:
    string_factory_instance = StringFactory(payload.value)
    stored_payload = string_factory_instance.create_response_payload()
    return { "paylaod": stored_payload }