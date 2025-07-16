import os
import json
import shutil
from subprocess import PIPE, run
import sys


Game_Dir_Pattern = 'game'

def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if Game_Dir_Pattern in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)



    return game_paths





def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    print(game_paths)


    create_dir(target_path)
    new_game_dirs = get_name_from_paths(game_paths, Game_Dir_Pattern)
    print(new_game_dirs)

if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) != 3:
        raise Exception("Must have a source and a target directory")

    source, target = sys.argv[1:]
    main(source, target)


