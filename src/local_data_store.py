###########################################################################################
# A simple in-memory data store that acts as a local Redis-like storage for storing       #
# key-value pairs.                                                                        #
#                                                                                         #
# Attributes:                                                                             #
#     db (dict): A dictionary to store the key-value pairs in memory.                     #
###########################################################################################

class LocalDataStore:
    #######################################################################################
    # Initializes the LocalDataStore instance with an empty in-memory database.           #
    #######################################################################################
    def __init__(self):
        self.db = {}

    #######################################################################################
    # Commits a payload to the database using a hash string as the key.                   #
    # If the hash string already exists, the method returns True without overwriting.     #
    #                                                                                     #
    # Args:                                                                               #
    #     hash_string (str): The hash string to use as the key.                           #
    #     payload: The value to store in the database.                                    #
    #                                                                                     #
    # Returns:                                                                            #
    #     bool: True if the key already exists, False if the payload was added.           #
    #######################################################################################
    def commit_to_db(self, hash_string: str, payload):
        if hash_string in self.db:
            return True
        else:
            self.db[hash_string] = payload
            return False

    #######################################################################################
    # Deletes a payload from the database by its hash string.                             #
    #                                                                                     #
    # Args:                                                                               #
    #     hash_string (str): The hash string to locate and delete the payload.            #
    #                                                                                     #
    # Returns:                                                                            #
    #     bool: True if the payload was successfully deleted, False otherwise.            #
    #######################################################################################
    async def delete_from_db(self, hash_string: str) -> bool:
        if hash_string in self.db:
            del self.db[hash_string]
            return True
        else:
            return False

    #######################################################################################
    # Retrieves a payload from the database by its hash string.                           #
    #                                                                                     #
    # Args:                                                                               #
    #     hash_string (str): The hash string to locate the payload.                       #
    #                                                                                     #
    # Returns:                                                                            #
    #     The payload if found, or None if the key does not exist.                        #
    #######################################################################################
    async def retrieve_from_db(self, hash_string: str):
        if hash_string in self.db:
            return self.db.get(hash_string)
        else:
            return None

    #######################################################################################
    # Retrieves the entire content of the in-memory database.                             #
    #                                                                                     #
    # Returns:                                                                            #
    #     dict: The entire database content as a dictionary.                              #
    #######################################################################################
    async def get_all_db_content(self):
        return self.db
