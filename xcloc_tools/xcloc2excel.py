import argparse
from pathlib import Path
from parsers import XclocParser
from generators import ExcelGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Xcloc to Excel.')
    parser.add_argument('file', type=Path, help='Xcloc file')
    args = parser.parse_args()

    parser = XclocParser(args.file)
    contents = parser.parse()

    generator = ExcelGenerator(contents)
    output = generator.generate()

    print("Convert finished successfully: {}".format(output))
