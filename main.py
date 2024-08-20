#!/usr/bin/env python3

from ptcl import *

import argparse
import sys

def main():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            "PTCL Color Tool", description="A tool to not have to hex edit color changes for PTCL files (but also not a proper editor)"
        )
        parser.add_argument("action", type=str, nargs="?",
                            help="The action to perform, either extract or apply")
        parser.add_argument("ptcl_path", type=str, nargs="?",
                            help="Path to the PTCL file to extract info from/to edit")
        parser.add_argument("json_path", type=str, nargs="?", default="",
                            help="Path to the JSON file with the changes to apply")
        args = parser.parse_args()

        if args.action == "extract":
            result = dump_json(args.ptcl_path, args.json_path)
        else:
            result = apply_edits(args.ptcl_path, args.json_path)
    else:
        option = input("Extract Info (1) or Apply Edits (2)?: ")
        if option not in ["1", "2"]:
            print("Invalid option, please enter 1 or 2")
            return
        ptcl_path = input("Enter path to decompressed PTCL or esetb.byml file: ")
        if option == "1":
            json_path = input("Enter output JSON path (optional, press ENTER to skip): ")
            result = dump_json(ptcl_path, json_path)
        else:
            json_path = input("Enter input JSON path (the file with the edits to apply): ")
            result = dump_json(ptcl_path, json_path)

    print(f"The requested operation {'was successful' if result else 'failed'}")

if __name__ == "__main__":
    main()