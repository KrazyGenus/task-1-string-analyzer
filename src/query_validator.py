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

def get_validated_filters(dict_object) -> Dict[str, Any]:
    converted_dict = {}
    print(dict_object)
    try:
        for key, value in dict_object.items():
            if value is None or not hasattr(value, '__len__') or len(value) == 0:
                raise ValueError
            if key == 'is_palindrome':
                try:
                    value = bool(value)
                    converted_dict[key] = value
                except (ValueError, TypeError):
                    raise TypeError

            elif key == 'min_length':
                try:
                    value = int(value)
                    converted_dict[key] = value
                except (ValueError, TypeError):
                    raise TypeError
            
            elif key == 'max_length':
                try:
                    value = int(value)
                    converted_dict[key] = value
                except (ValueError, TypeError):
                    raise TypeError
            
            elif key == "word_count":
                try:
                    value = int(value)
                    converted_dict[key] = value
                except (ValueError, TypeError):
                    raise TypeError
            elif key == 'contains_character':
                if isinstance(value, str) and len(value) == 1:
                    converted_dict[key] = value
                else:
                    raise TypeError
            
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query parameters",
        )
    return converted_dict