import os
MAX_CHAR = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    """Read up to MAX_CHAR characters of `file_path`, relative to the
    sandboxed working directory."""
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Guard against path traversal (e.g. "../../etc/passwd") before opening.
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

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads a file content up to 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to a file that we want to read the contents of if it is in the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}
