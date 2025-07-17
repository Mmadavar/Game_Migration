import os
import json
import shutil
from subprocess import PIPE, run
import sys


Game_Dir_Pattern = 'game'
GAME_CODE_EXTENSION = '.go'
GAME_COMPILE_COMMAND = ["go", "build"]
def find_all_game_paths(source):
    game_paths = []
    #os.walk allows us to go to the source path in a recursivel process
    #
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            # add path to the game paths
            if Game_Dir_Pattern in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths

def copy_and_overwrite(source, destination):
    #shutil.rmtree recursively finds the path to remove
    #copytree recursively copies the directory tree from the source to the destination
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def create_dir(path):
    # if path doesn't exist use mkdir to make the directory
    if not os.path.exists(path):
        os.mkdir(path)

def get_name_from_paths(paths, to_strip):
    # split the path into the directory and the parent directory
    # replace the string to_strip that we pass and the empty string will get rid of it from the directory
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def make_json_metadata_file(path, game_dirs):
    data = {
        "game_names": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    # w stand for write and override the file if it exists
    #json.dump dumps the data into the file
    # if we didn't use with we would have to manually close the file and some problems can occur.
    # when using open it's used as a context manager
    with open(path, "w") as f:
        json.dump(data, f)


def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION) in file:
                code_file_name = file
                break
        break

    if code_file_name is None:
        return

    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)

def run_command(command, path):
    cwd = os.getcwd()
    # change working directory into the path
    os.chdir(path)
    # stdout and stdin is location where command is accepting input and output and PIPE makes the bridge
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("Compile result", result)

    # good practice to change the directory to the current working directory
    os.chdir(cwd)


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)

    new_game_dirs = get_name_from_paths(game_paths, "_game")

    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "get_game_data.json")
    make_json_metadata_file(json_path, new_game_dirs)





 

if __name__ == "__main__":
    # sys.argv registers the amount of arguments from the command line
    args = sys.argv
    print(args)
    if len(args) != 3:
        raise Exception("Must have a source and a target directory")

    # use 1: to strip off the name of our python file which we don't want and store the 2 arguments.
    source, target = sys.argv[1:]
    main(source, target)


