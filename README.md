# String Analyzer API

This project is a FastAPI-based web application for analyzing and managing strings. It provides various endpoints to perform operations such as adding, retrieving, filtering, and deleting strings. Configuration management is handled using the `uv` library.

## Endpoints

### 1. Add a String
**POST** `/strings`  
Add a new string to the system.

### 2. Retrieve a String
**GET** `/strings/{string_value}`  
Retrieve details about a specific string.

### 3. Filter Strings by Attributes
**GET** `/strings`  
Filter strings based on the following query parameters:
- `is_palindrome` (optional): Filter strings that are palindromes (`true` or `false`).
- `min_length` (optional): Minimum length of the string.
- `max_length` (optional): Maximum length of the string.
- `word_count` (optional): Number of words in the string.
- `contains_character` (optional): Filter strings containing a specific character.

Example:  
`GET /strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a`

### 4. Filter Strings by Natural Language Query
**GET** `/strings/filter-by-natural-language`  
Filter strings using a natural language query.  
Query parameter:
- `query`: A natural language description of the filter criteria.

Example:  
`GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings`

### 5. Delete a String
**DELETE** `/strings/{string_value}`  
Delete a specific string from the system.

## Configuration
The application uses the `uv` library for managing configuration. Ensure that the necessary configuration files are set up before running the application.

## Installing uv
```bash
    pip install uv
```
## Running the Application
1. Install dependencies using `uv`:
    ```bash
    uv install
    ```
2. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
3. Access the API documentation at:  
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## License
This project is licensed under the MIT License.