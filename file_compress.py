import glob
import os
from gs_compress import *
import pandas as pd
import argparse


def file_compress(src):

    # concatenate "<src> + _Reduced" to form compression destination directory
    dest_base = src.rstrip('\/') + '_Reduced'
    if os.path.exists(dest_base):
        shutil.rmtree(dest_base) # remove existing directory for first run / another attempt

    rows=[]
    search = os.path.join(src, '**')
    for file in glob.glob(search, recursive=True):
        if file.endswith('.pdf') and not os.path.isdir(file): # could expand this someday to include images

            file_abs = os.path.abspath(file)  # absolute file path
            file_rel = os.path.relpath(file, src)  # file path relative to src

            file_name = file_rel.split('/')[-1]  # everything after last '/'

            file_size = os.path.getsize(file_abs) / (1024 * 1024)  # convert bytes to megabytes
            file_size = round(file_size, 2)  # 2 == precision after decimal

            # only compress files > 5 MB
            if file_size > 5:

                file_abs_compressed = os.path.join(dest_base, file_rel)
                file_abs_compressed = os.path.abspath(file_abs_compressed)  # must be absolute for ghostcript

                # in case file is in sub-folder
                dest = os.path.dirname(file_abs_compressed)

                # ghost script will throw up if compression destination directories do not exist
                if not os.path.exists(dest):
                    os.system(f'mkdir -p "{dest}"')  # don't know the equivalent in python

                if os.path.exists(file_abs):
                    info = compress(file_abs, file_abs_compressed, 4)

                    rows.append(
                        [file_name, info[0], info[1], info[2]])

    df = pd.DataFrame(rows,
                      columns=['File', 'Initial Size (MB)', 'Final Size (MB)', 'Compression Ratio (%)'])
    print(df)

    # export dataframe to csv file
    df.to_csv('pdf_compress.csv', sep=',', encoding='utf-8')


def main():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('src', help='Path to file directory in need of compression')
    args = parser.parse_args()

    # Run
    file_compress(args.src)


if __name__ == "__main__":
    # Executed when invoked directly, ie. `python file_compress.py`
    main()
