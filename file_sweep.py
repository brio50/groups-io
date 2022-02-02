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
            if 'manual' in file_name.lower() or 'manual' in json_desc.lower():
                category = 'manual'
            elif 'brochure' in file_name.lower() or 'brochure' in json_desc.lower():
                category = 'brochure'
            elif 'bulletin' in file_name.lower() or 'bulletin' in json_desc.lower():
                category = 'brochure'
            elif 'gear' in file_name.lower() or 'gear' in json_desc.lower():
                category = 'threading'
            elif 'thread' in file_name.lower() or 'thread' in json_desc.lower():
                category = 'threading'
            elif 'serial' in file_name.lower() or 'serial' in json_desc.lower():
                category = 'history'
            elif 'patent' in file_name.lower() or 'patent' in json_desc.lower():
                category = 'history'
            elif 'drawing' in file_name.lower() or 'drawing' in json_desc.lower():
                category = 'drawing'
            elif 'assembly' in file_name.lower() or 'assembly' in json_desc.lower():
                category = 'drawing'
            elif 'wiring' in file_name.lower() or 'wiring' in json_desc.lower():
                category = 'electrical'
            elif 'schematic' in file_name.lower() or 'schematic' in json_desc.lower():
                category = 'electrical'
            elif 'circuit' in file_name.lower() or 'circuit' in json_desc.lower():
                category = 'electrical'
            else:
                category = ''

            # model search - case sensitive
            model = []
            if 'AHC' in file_rel:
                model.append('AHC')
            if 'DV59' in file_rel:
                model.append('DV59')
            if 'HC' in file_rel:
                model.append('HC')
            if 'HCT' in file_rel:
                model.append('HCT')
            if 'HLV' in file_rel:
                model.append('HLV')
            if 'TL' in file_rel:
                model.append('TL')
            if 'T-10' in file_rel:
                model.append('T-10')
            if 'TM' in file_rel:
                model.append('TM')
            if 'UM' in file_rel:
                model.append('UM')

            # convert to semi-colon separated list for csv
            model = ";".join(model)

            # save row off
            rows.append([file_rel, file_url, file_ext, file_size, json_created, json_desc, category, model, 'Y', ''])

    df = pd.DataFrame(rows,
                      columns=['File', 'URL', 'Extension', 'Size (MB)', 'Created', 'Description', 'Category', 'Model',
                               'Keep (Y/N)', 'Note'])
    print(df)

    # export dataframe to csv file
    df.to_csv('file_sweep.csv', sep=',', encoding='utf-8')


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
