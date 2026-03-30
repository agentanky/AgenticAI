import os
import subprocess
import time
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    pathNormalized = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(pathNormalized, file_path))

    valid_target_file_path = os.path.commonpath([pathNormalized, target_file_path]) == pathNormalized
    valid_file_path = os.path.isfile(target_file_path)
    if not valid_file_path:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not valid_target_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file_path]
    if args:
        command.extend(args)
    try:
        result = subprocess.run(command, cwd=pathNormalized, capture_output=True, text=True, timeout= 30  )
    except Exception as e:
       return (f"Error: executing Python file: {e}")
    outputString = ""
    if result.returncode != 0:
        outputString += f"Process exited with code {result.returncode}"
    elif not result.stdout and not result.stderr:
        outputString += "No output produced"
    else:
        if result.stdout:
            outputString += f"STDOUT: {result.stdout}"
        if result.stderr:
            outputString += f"STDERR: {result.stderr}"
    return outputString
     
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the file_path file ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path of the file that will be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="additional arguments with a default of None",
            ),
        },
    ),
)