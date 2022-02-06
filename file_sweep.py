import glob
import os
import json
import pandas as pd
import argparse


def json_read(file_abs):

    json_name = file_abs + ".json"
    if not os.path.exists(json_name):
        raise Exception(f"JSON file does not exist: {json_name}")

    # key assumption: for every "file.ext," "file.ext.json" exists
    # this seems to be the behavior for groups.io aws file or photo dump/backup according to
    json_file = open(json_name, 'r')
    json_val = json.load(json_file)
    json_file.close()

    # key assumption: every .json file contains 'Created' and 'Desc' variables
    json_created = json_val['Created']
    json_name = json_val['Name']
    json_desc = json_val['Desc']

    # remove tabs and newlines
    json_desc = ' '.join(json_desc.split())

    return {'created': json_created, 'name': json_name, 'desc': json_desc}


def file_sweep(src, url_base):

    rows = []
    search = os.path.join(src, '**')
    files = sorted(glob.glob(search, recursive=True))  # sort alphanumerically
    for file in files:
        if ".json" not in file and not os.path.isdir(file):

            file_abs = os.path.abspath(file)  # absolute file path
            file_rel = os.path.relpath(file, src)  # file path relative to src

            file_url = url_base + file_rel
            file_url = file_url.replace('\\', '/')  # in case we're running in windows
            file_url = file_url.replace(" ", "%20")  # urls use %20 in space

            file_name = file_rel.split(os.sep)[-1]  # everything after last '/'
            file_ext = os.path.splitext(file)[1]  # get file extension only

            file_size = os.path.getsize(file_abs) / (1024 * 1024)  # convert bytes to megabytes
            file_size = round(file_size, 2)  # 2 == precison after decimal

            json_dict = json_read(file_abs)
            json_name = json_dict['name']
            json_created = json_dict['created']
            json_desc = json_dict['desc']

            # compare
            if not file_name == json_name:
                raise Exception(f"File Name and Json Names are not equal\n{file_name}\n{json_name}")

            # category search - case insensitive - within file name and description
            fields = [file_name.lower(), json_desc.lower()]
            if 'manual' in str(fields):
                category = 'manual'
            elif 'parts' in str(fields):
                category = 'manual'
            elif 'brochure' in str(fields):
                category = 'brochure'
            elif 'bulletin' in str(fields):
                category = 'brochure'
            elif 'gear' in str(fields):
                category = 'gearing'
            elif 'thread' in str(fields):
                category = 'gearing'
            elif 'serial' in str(fields):
                category = 'history'
            elif 'patent' in str(fields):
                category = 'history'
            elif 'drawing' in str(fields):
                category = 'drawing'
            elif 'assembly' in str(fields):
                category = 'drawing'
            elif 'wiring' in str(fields):
                category = 'electrical'
            elif 'schematic' in str(fields):
                category = 'electrical'
            elif 'circuit' in str(fields):
                category = 'electrical'
            else:
                category = ''

            # model search - case sensitive
            fields = [file_rel, json_desc]
            if 'cataract' in str(fields).lower():
                model = 'CATARACT'
            elif 'AHC' in str(fields):
                model = 'AHC'
            elif 'HC' in str(fields):
                model = 'HC'
            elif 'DV' in str(fields):
                model = 'DV+DSM'
            elif 'DSM' in str(fields):
                model = 'DV+DSM'
            elif 'HLV-H' in str(fields):
                model = 'HLV-H'
            elif 'HLV' in str(fields):
                model = 'HLV'
            elif 'TR' in str(fields):
                model = 'TR+ESM'
            elif 'ESM' in str(fields):
                model = 'TR+ESM'
            elif 'TL' in str(fields):
                model = 'TL'
            elif 'T-10' in str(fields):
                model = 'TL'
            elif 'T10' in str(fields):
                model = 'TL'
            elif 'T-5' in str(fields):
                model = 'TL'
            elif 'T5' in str(fields):
                model = 'TL'
            elif 'CNC' in str(fields):
                model = 'CNC'
            else:
                model = ''

            # save row off
            rows.append([file_rel, file_url, file_ext, file_size, json_created, json_desc, category, model, 'Y', ''])

    df = pd.DataFrame(rows,
                      columns=['File', 'URL', 'Extension', 'Size (MB)', 'Created', 'Description', 'Category', 'Model',
                               'Keep (Y/N)', 'Note'])
    print(df)

    # export dataframe to csv file
    df.to_csv('file_sweep.csv', sep=',', encoding='utf-8')

    df.to_json('file_sweep.json')

def main():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('src', help='Path to file directory in need of sweeping')
    parser.add_argument('url_base', help='groups.io base url; concatenated with file names')
    args = parser.parse_args()

    # Run
    file_sweep(args.src, args.url_base)


if __name__ == "__main__":
    # Executed when invoked directly, ie. `python file_sweep.py`
    main()
