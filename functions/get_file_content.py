import sys
from google.genai import types
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_dir = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(target_file_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="File path to get the content of a file from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)