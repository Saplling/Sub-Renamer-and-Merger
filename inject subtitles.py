import os
from pathlib import Path
from sys import argv
import subprocess

def get_file_paths_of_type(directory: str, file_type:str) -> list[str]:
    fileNamesStr = os.listdir(directory) 
    filePaths = [Path(directory).joinpath(name_string) for name_string in fileNamesStr if Path(name_string).suffix == file_type] #Turns strings into path objects while making sure they're mkv's
    return filePaths


def main(args:list[str]):
    mkv_dir, subs_dir, output_dir = args[1], args[2], args[3]
    language = []
    if args[4] == "jp":
        language = ["--language", "0:ja", "--track-name", "0:Japanese"]
    elif args[4] == "en":
        language = ["--language", "0:en", "--track-name", "0:English"]

    mkv_paths: list[Path] = get_file_paths_of_type(mkv_dir, ".mkv")
    sub_paths: list[Path] = get_file_paths_of_type(subs_dir, ".ass")
    if len(mkv_paths) != len(sub_paths):
        print("Mismatch in file amounts. Possiblity of missing some files...")
    for mkv_path, sub_path in zip(mkv_paths, sub_paths):
        output_path = Path(output_dir).joinpath(mkv_path.name)
        command = [
            r"C:\Program Files\MKVToolNix\mkvmerge.exe",
            "-o",
            output_path,
            mkv_path,
            sub_path
        ]
        if language: command[0:4].extend
        subprocess.run(command)


class InvalidNumberOfArgumentsError(ValueError):
    pass

if __name__ == "__main__":
    if len(argv) > 5:
        raise InvalidNumberOfArgumentsError("Too many or not enough arguments!\nFormat: [video dir] [subs dir] [output dir] [sub language]")
    main(argv)
