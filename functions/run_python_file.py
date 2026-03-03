import sys
import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_abs, file_path))

        valid_target_dir = os.path.commonpath([working_directory_abs, target_file_path]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args and len(args) > 1:
            command.extend(args[1:])
        
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_parts = []

        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        stdout_content = completed_process.stdout.strip()
        stderr_content = completed_process.stderr.strip()
        
        if not completed_process.stdout.strip() and not completed_process.stderr.strip():
            output_parts.append("No output produced")
        else:
            if completed_process.stdout.strip():
                output_parts.append(f"STDOUT:\n{completed_process.stdout.strip()}")
            if completed_process.stderr.strip():
                output_parts.append(f"STDERR:\n{completed_process.stderr.strip()}")
        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python script in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="File path to run python script from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)