import os

def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs = os.path.abspath(working_directory)

        target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))

        valid_target_dir = os.path.commonpath([working_directory_abs, target_directory]) == working_directory_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_directory):
            return f'Error: Cannot list "{directory}" is not a directory'

    
        lines = []
        for document in sorted(os.listdir(target_directory)):
            full_path = os.path.join(target_directory, document)

            file_size =os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)

            line = f"- {document}: file_size={file_size} bytes, is_dir={is_dir}"
            lines.append(line)
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"