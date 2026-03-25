import os

def get_files_info(working_directory, directory=""):
    pathNormalized = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(pathNormalized, directory))

    valid_target_dir = os.path.commonpath([pathNormalized, target_dir]) == pathNormalized
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    results = []
    for item in os.listdir(target_dir ):
        full_path = os.path.join(target_dir , item)
        size = os.path.getsize(full_path)
        is_dir = os.path.isdir(full_path)
        results.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
    return "\n".join(results)