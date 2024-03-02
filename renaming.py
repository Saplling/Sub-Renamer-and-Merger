import os
import pathlib
from sys import argv
import re 

def get_mkv_file_names(directory: str) -> list[str]:
    fileNamesStr = os.listdir(directory) 
    filePaths = [pathlib.Path(name_string) for name_string in fileNamesStr if pathlib.Path(name_string).suffix == ".mkv"] #Turns strings into path objects while making sure they're mkv's
    mkv_file_names = [path.stem for path in filePaths] #remove extention 
    return mkv_file_names

def sorting_key(input: str):
    one_or_two_nums = re.compile(r"\d*")
    list_of_all_nums = sorted([match for match in one_or_two_nums.findall(input) if match and len(match) <= 2], key=len)
    if not list_of_all_nums:
        return 0
    return int(list_of_all_nums[-1])




def rename_files_in_dir(directory: str, new_names:list[str]):
    parent_directory = pathlib.Path(directory)
    file_names = sorted([file_name for file_name in os.listdir(directory) if pathlib.Path(file_name).suffix in (".ass", ".srt")], key=sorting_key)
    print(file_names)
    file_paths = [pathlib.Path.joinpath(parent_directory, file_name) for file_name in file_names]
    if not file_paths:
        raise Exception("No Subtitle files found... (Must be srt or ass file)")
    files_suffix = file_paths[0].suffix
    if len(file_paths) != len(new_names):
        raise Exception(f"""
                        Mismatching amount of files
                        sub files:{len(file_paths)}
                        mkv files:{len(new_names)}
                        """)
    for file, new_name in zip(file_paths, new_names):
        new_sub_path_with_name = f"{directory}\\{new_name}{files_suffix}"
        os.rename(file, new_sub_path_with_name)

def main():
    _, mkv_dir, subs_dir = argv
    #Manual Override Testing
    # mkv_dir = r"F:\ANime\[Judas] Oshi no Ko (Season 1) [1080p][HEVC x265 10bit][Eng-Subs]"
    # subs_dir = r"F:\ANime\[Judas] Oshi no Ko (Season 1) [1080p][HEVC x265 10bit][Eng-Subs]\Subs"
    new_names = get_mkv_file_names(mkv_dir)
    rename_files_in_dir(subs_dir, new_names)

if __name__ == "__main__":
    main()


