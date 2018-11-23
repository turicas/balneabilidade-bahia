import argparse
import os

import rows
import rows.utils

from ba_parse_pdf import extract_table as ba_extract_table
from sc_parse_pdf import extract_table as sc_extract_table


extract_table_functions = {"BA": ba_extract_table, "SC": sc_extract_table}
parser = argparse.ArgumentParser()
parser.add_argument("state", choices=["BA", "SC"])
parser.add_argument("input_uri")
parser.add_argument("output_filename")
args = parser.parse_args()

input_uri, delete = args.input_uri, False
if input_uri.lower().startswith("http://") or input_uri.lower().startswith("https://"):
    source = rows.utils.download_file(input_uri, progress=True, detect=False)
    input_uri, delete = source.uri, True

data = extract_table_functions[args.state](input_uri)
table = rows.import_from_dicts(data)
rows.export_to_csv(table, args.output_filename)
if delete:
    os.unlink(input_uri)
