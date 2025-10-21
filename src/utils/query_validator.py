from fastapi import HTTPException, status
from typing import Dict, Any


###########################################################################################
# Validates the query parameters for filtering strings.                                   #
# Ensures that all parameters meet the required type and value constraints.              #
# Args:                                                                                   #
#     is_palindrome (bool): Indicates if the string should be a palindrome.               #
#     min_length (int): The minimum length of the string.                                 #
#     max_length (int): The maximum length of the string.                                 #
#     word_count (int): The number of words in the string.                                #
#     contains_character (str): A single character that must be present in the string.    #
# Returns:                                                                                #
#     Dict[str, Any]: A dictionary containing the validated query parameters.             #
# Raises:                                                                                 #
#     HTTPException: If any of the query parameters are invalid.                          #
###########################################################################################

def get_validated_filters(
    is_palindrome,
    min_length,
    max_length,
    word_count,
    contains_character
) -> Dict[str, Any]:
    
    errors = []
    
    # Validate is_palindrome: must be a boolean
    if is_palindrome is None or type(is_palindrome) is not bool:
        errors.append("is_palindrome must be a boolean value (true/false)")
    
    # Validate min_length: must be a positive integer
    if min_length is None or type(min_length) is not int:
        errors.append("min_length must be an integer")
    elif min_length <= 0:
        errors.append("min_length must be a positive integer")
    
    # Validate max_length: must be a positive integer
    if max_length is None or type(max_length) is not int:
        errors.append("max_length must be an integer")
    elif max_length <= 0:
        errors.append("max_length must be a positive integer")
    
    # Validate word_count: must be a positive integer
    if word_count is None or type(word_count) is not int:
        errors.append("word_count must be an integer")
    elif word_count <= 0:
        errors.append("word_count must be a positive integer")
    
    # Validate contains_character: must be a single non-empty character
    if contains_character is None or type(contains_character) is not str:
        errors.append("contains_character must be a string")
    elif len(contains_character) == 0:
        errors.append("contains_character cannot be empty")
    elif len(contains_character) > 1:
        errors.append("contains_character must be a single character")
    
    # Raise an HTTPException if there are validation errors
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query parameters",
        )
    
    # Return the validated query parameters as a dictionary
    return {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }
