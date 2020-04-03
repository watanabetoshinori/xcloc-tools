import argparse
from pathlib import Path
from parsers import ExcelParser
from generators import XclocGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Excel to Xcloc.')
    parser.add_argument('file', type=Path, help='Excel file')
    args = parser.parse_args()

    parser = ExcelParser(args.file)
    contents = parser.parse()

    generator = XclocGenerator(contents)
    output = generator.generate()

    print("Convert finished successfully: {}".format(output))
