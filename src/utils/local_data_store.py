"""
    A simple in-memory data store that acts as a local Redis-like storage for storing key-value pairs.

    Attributes:
        db (dict): A dictionary to store the key-value pairs in memory.
"""

class LocalDataStore:
    def __init__(self):
        self.db = {}
    
    def commit_to_db(self, hash_string:str, payload):
        if hash_string in self.db:
            return True
        else:
            self.db[hash_string] = payload
            return False




    async def delete_from_db(self, hash_string:str) -> bool:
        if hash_string in self.db:
            del self.db[hash_string]
            return True
        else:
            return False


    async def retrieve_from_db(self, hash_string:str):
        if hash_string in self.db:
            return self.db.get(hash_string)
        else:
            return None
    
    async def get_all_db_content(self):
        return self.db

