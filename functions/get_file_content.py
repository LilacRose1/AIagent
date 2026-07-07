import os
MAX_CHAR = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if(valid_file == False):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        if(os.path.isfile(target_file) == False):
            return f"Error: File not found or is not a regular file: \"{file_path}\""

        with open(target_file, "r") as file:
            file_string = file.read(MAX_CHAR)

            if file.read(1):
                file_string += f"[...File \"{file_path}\" truncated at {MAX_CHAR} characters]"

        return file_string


    except Exception as e:
        return f"Error: {e}";

