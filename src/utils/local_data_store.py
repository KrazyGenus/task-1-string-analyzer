"""
    A simple in-memory data store that acts as a local Redis-like storage for storing key-value pairs.

    Attributes:
        db (dict): A dictionary to store the key-value pairs in memory.
"""

class LocalDataStore:
    def __init__(self):
        self.db = {}
    
    def commit_to_db(self, hash_string:str, payload):
        if hash_string not in self.db:
            self.db[hash_string] = payload
        # check for when the key exists
        print(f"In LocalDB {self.db.get(hash_string)}")




    def delete_from_db(self, hash_string:str):
        pass
    def retrieve_from_db(self, hash_string:str):
        pass
