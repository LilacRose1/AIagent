import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if(valid_dir == False):
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

        if(valid_dir == True):
            if(directory != "."):
                output_string = f"Result for \'{directory}\' directory:\n"
            else:
                output_string = f"Result for current directory:\n"
            for file in os.listdir(target_dir):
                name = file
                file_size = os.path.getsize(os.path.join(target_dir, file))
                is_dir = os.path.isdir(os.path.join(target_dir, file))
                output_string += f"- {name}: file_size={file_size} bytes, is_dir={is_dir}\n"

            return output_string


    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
