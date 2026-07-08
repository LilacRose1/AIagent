import os 
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if(valid_file == False):
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        elif(os.path.isfile(target_file) == False):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        elif(not file_path.endswith(".py")):
            return f"Error: \"{file_path}\" is not a Python file"

        command = ["python", target_file]

        if(args != None):
            command.extend(args)

        run_command = subprocess.run(command, capture_output=True, text=True, timeout= 30)

        output_string = ""

        if(run_command.returncode != 0):
            output_string += f"Process exited with code {run_command.returncode}\n"

        if(run_command.stdout == None and run_command.stderr == None):
            output_string += f"No output produced"
        else:
            output_string += f"STDOUT: {run_command.stdout}\nSTDERR: {run_command.stderr}\n"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
