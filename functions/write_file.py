import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_dir = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        target_dir = os.path.dirname(target_file_path)

        os.makedirs(target_dir, exist_ok = True)

        with open(target_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)