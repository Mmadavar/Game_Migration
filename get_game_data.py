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


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    print(game_paths)

if __name__ == "__main__":
    args = sys.argv
    print(args)
    if len(args) != 3:
        raise Exception("Must have a source and a target directory")

    source, target = sys.argv[1:]
    main(source, target)


