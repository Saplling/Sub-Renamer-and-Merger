import os
from pathlib import Path
from sys import argv
import subprocess
import re 


def sorting_key(input: str):
    one_or_two_nums = re.compile(r"\d*")
    list_of_all_nums = sorted([match for match in one_or_two_nums.findall(input) if match and len(match) <= 2], key=len)
    if not list_of_all_nums:
        return 0
    return int(list_of_all_nums[-1])

def get_file_paths_of_type(directory: str, file_type:tuple[str]) -> list[str]:
    fileNamesStr = os.listdir(directory) 
    fileNames = sorted([name_string for name_string in fileNamesStr if Path(name_string).suffix in file_type], key=sorting_key)
    filePaths = [Path(directory).joinpath(name_string) for name_string in fileNames]
    return filePaths


def main(args:list[str]):
    mkv_dir, subs_dir, output_dir = args[1], args[2], args[3]
    language = []
    if args[4] == "jp":
        language = ["--language", "0:ja", "--track-name", "0:Japanese"]
    elif args[4] == "en":
        language = ["--language", "0:en", "--track-name", "0:English"]

    mkv_paths: list[Path] = get_file_paths_of_type(mkv_dir, (".mkv",))
    sub_paths: list[Path] = get_file_paths_of_type(subs_dir, (".ass", ".srt"))
    if len(mkv_paths) != len(sub_paths):
        print("Mismatch in file amounts. Possiblity of missing some files...")
    for mkv_path, sub_path in zip(mkv_paths, sub_paths):
        output_path = Path(output_dir).joinpath(mkv_path.name)
        command = [
            r"C:\Program Files\MKVToolNix\mkvmerge.exe",
            "-o",
            output_path,
            mkv_path
        ]
        if language: command.extend(language)
        command.append(sub_path)
        subprocess.run(command)


class InvalidNumberOfArgumentsError(ValueError):
    pass

if __name__ == "__main__":
    # print(len(argv))
    # argv = ["", "F:\ANime\[Judas] Re.Zero kara Hajimeru Isekai Seikatsu (Season 2 Part 1) [1080p][HEVC x265 10bit][Multi-Subs]", "F:\ANime\[Judas] Re.Zero kara Hajimeru Isekai Seikatsu (Season 2 Part 1) [1080p][HEVC x265 10bit][Multi-Subs]\Subs", "F:\ANime\[Judas] Re.Zero kara Hajimeru Isekai Seikatsu (Season 2 Part 1) [1080p][HEVC x265 10bit][Multi-Subs]\Merged Videos", "jp"]
    if len(argv) > 5 or len(argv) < 4:
        raise InvalidNumberOfArgumentsError("Too many or not enough arguments!\nFormat: [video dir] [subs dir] [output dir] optional:[sub language]")
    main(argv)
