from os import listdir
from pathlib import Path
from sys import argv
from subprocess import run
from re import compile

class InvalidNumberOfArgumentsError(ValueError):
    DEFAULT_MESSAGE = "Too many or not enough arguments!"
    def __init__(self, message:str=DEFAULT_MESSAGE) -> None:
        self.message = message
        super().__init__(self.message)


def main(args: list[str]):
    if len(args) not in (2, 4, 5, 6):
        raise InvalidNumberOfArgumentsError()
    
    rest_of_args = args[2:]
    if args[1] == "1":
        injecter(rest_of_args)
    elif args[1] == "0":
        renamer(rest_of_args)
    else:
        menu(agrs)


if __name__ == "__main__":
    main(argv)