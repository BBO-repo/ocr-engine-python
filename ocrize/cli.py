from os import path
from argparse import ArgumentParser, RawTextHelpFormatter
import ocrlib


def is_valid_file(parser, arg) -> str :
    if not path.isfile(arg):
        parser.error("The file %s does not exist!"%arg)
    else:
        return arg

def main() -> None :
    parser = ArgumentParser(prog='ocrize',formatter_class=RawTextHelpFormatter)
    parser.add_argument('-t', '--type', required=True, type=int, choices=[1, 2, 3],
                        help="Type of the document.\n"
                        "Possible value are:\n"
                        "1: insurance card photo\n"
                        "2: unilabs pdf document\n"
                        "3: dianalabs pdf document")
    parser.add_argument('-p', '--path', required=True, type=lambda x: is_valid_file(parser, x), help="Path to the document")
    args = parser.parse_args()
    ocrlib.Ocrizer.process(args.path, ocrlib.DocType(args.type)) 
    

if __name__ == '__main__':
    main()
