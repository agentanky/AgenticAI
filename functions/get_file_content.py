import os
from google.genai import types

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    pathNormalized = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(pathNormalized, file_path))

    valid_target_file_path = os.path.commonpath([pathNormalized, target_file_path]) == pathNormalized
    valid_file_path = os.path.isfile(target_file_path)
    if not valid_file_path:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not valid_target_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(target_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets content of a file provided the file path is within a working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path of the file that contents will be read from",
            ),
        },
    ),
)