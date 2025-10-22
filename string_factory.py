"""
Using a full-fledged database for this task would be overkill. 
Instead, we will use a dictionary data structure to store the data, where:
- The key is the hash of the string.
- The value is a dictionary containing the required properties of the string.

EXAMPLE STRUCTURE OF THE DATA STORED:
{
    "id": "sha256_hash_value",  # Unique identifier (hash) for the string
    "value": "string to analyze",  # The original string
    "properties": {  # Various properties of the string
        "length": 16,  # Length of the string
        "is_palindrome": false,  # Whether the string is a palindrome
        "unique_characters": 12,  # Count of unique characters
        "word_count": 3,  # Number of words in the string
        "sha256_hash": "abc123...",  # SHA-256 hash of the string
        "character_frequency_map": {  # Frequency of each character
            "s": 2,
            "t": 3,
            "r": 2,
            // ... etc
        }
    },
    "created_at": "2025-08-27T10:00:00Z"  # Timestamp of when the data was created
}
"""

import hashlib
from datetime import datetime, timezone
from config import DB_INSTANCE_POOL
from fastapi import HTTPException, status

"""
    A utility class for handling and analyzing valid strings.

    Attributes:
        string (str): The valid string provided during initialization.
    
    Initializes the class with a valid string.

        Args:
            valid_string (str): The string to be stored and analyzed.
"""
class StringFactory:
    def __init__(self, valid_string):
        self.string = valid_string.lower()
    
  
#################################################
# @create_response_payload: creates a dictionary#
# containing the analyzed properties of the     #
# string, including its hash, length, etc.      #
# returns: a dictionary with the string's data  #
#################################################
    def create_response_payload(self) -> dict:
        utc_now = datetime.now(timezone.utc)
        iso_8601_utc_time = utc_now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        generated_hash = self.sha256_hash()

        payload = {
            "id": self.sha256_hash(),
            "value": self.string,
            "properties": {
                "length": self.length_of_string(),
                "is_palindrome": self.is_palindrome(),
                "unique_characters": self.unique_characters(),
                "word_count": self.word_count(),
                "sha256_hash": self.sha256_hash(),
                "character_frequency_map": self.character_frequency_map(),
            },
            "created_at": str(iso_8601_utc_time)
        }
        save_status = DB_INSTANCE_POOL.commit_to_db(generated_hash, payload)
        if save_status is not True:
            return payload
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="String already exists in the system"
            )
            
      
#################################################
# @length_of_string: calculates the length of   #
# the string                                    #
# returns: an integer representing the length   #
#################################################
    def length_of_string(self) -> int:
        return len(self.string)


      
##################################################
# @is_palindrome: checks palindrome of  a string #
# returns: a boolen True or False                #
#                                                #
##################################################
    def is_palindrome(self) -> bool:
        """
        Check if the string stored in the instance is a palindrome.

        A palindrome is a string that reads the same backward as forward.

        Returns:
            bool: True if the string is a palindrome, False otherwise.
        """
        start = 0
        end = len(self.string) - 1
        while start < end:
            if self.string[start] == self.string[end]:
                start += 1
                end -= 1
                continue
            else:
                return False
        return True





      
#################################################
# @unique_characters: count unique characters   #
# returns: an int of unique characters          #
#                                               #
#################################################
    def unique_characters(self) -> int:
        return len(set(self.string))

  
#################################################
# @word_count: number of words in a string      #
# returns: a str of the number of words         #
#                                               #
#################################################
    def word_count(self) -> int:
        words = self.string.split()
        return len(words)




#################################################
# @sha256_hash: hashes a string                 #
# returns: a string representation of the hash  #
#                                               #
#################################################
    def sha256_hash(self) -> str:
        # Convert the string to bytes using UTF-8 encoding,
        # as the hashing algorithm requires a byte input.
        byte_string = self.string.encode("utf-8")
        # Generate the SHA-256 hash of the byte-encoded string
        # and return its hexadecimal representation.
        return hashlib.sha256(byte_string).hexdigest()

    

  
####################################################
# @character_frequency_map: frequency of each word #
# returns: a dict containing the frequecnt of each #
# charcater in the given string                    #
#                                                  #
####################################################
    def character_frequency_map(self)-> dict:
        frequency_map = {}
        for char in self.string:
            if char not in frequency_map:
                frequency_map[char] = 1
            elif char in frequency_map:
                frequency_map[char] += 1
        return frequency_map
