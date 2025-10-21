from fastapi import HTTPException, status
from typing import Dict, Any




def get_validated_filters(
    is_palindrome,
    min_length,
    max_length,
    word_count,
    contains_character
) -> Dict[str, Any]:
    
    errors = []
    
    # Your validation logic (similar to above)
    if is_palindrome is None or type(is_palindrome) is not bool:
        errors.append("is_palindrome must be a boolean value (true/false)")
    
    if min_length is None or type(min_length) is not int:
        errors.append("min_length must be an integer")
    elif min_length <= 0:
        errors.append("min_length must be a positive integer")
    
    if max_length is None or type(max_length) is not int:
        errors.append("max_length must be an integer")
    elif max_length <= 0:
        errors.append("max_length must be a positive integer")
    
    if word_count is None or type(word_count) is not int:
        errors.append("word_count must be an integer")
    elif word_count <= 0:
        errors.append("word_count must be a positive integer")
    
    if contains_character is None or type(contains_character) is not str:
        errors.append("contains_character must be a string")
    elif len(contains_character) == 0:
        errors.append("contains_character cannot be empty")
    elif len(contains_character) > 1:
        errors.append("contains_character must be a single character")
    
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query parameters",
        )
    
    return {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }
