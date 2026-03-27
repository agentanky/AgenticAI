import os

def write_file(working_directory, file_path, content):
    pathNormalized = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(pathNormalized, file_path))

    valid_target_file_path = os.path.commonpath([pathNormalized, target_file_path]) == pathNormalized
    isDir = os.path.isdir(target_file_path)
    if isDir:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    if not valid_target_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    try:
        with open(target_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
        