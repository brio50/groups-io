import glob
import os
from gs_compress import *
import pandas as pd
import argparse


def file_reorg(src):

    # concatenate "<src> + _Reduced" to form compression destination directory
    dest_base = src.rstrip('\/') + '_Reorg'
    if os.path.exists(dest_base):
        shutil.rmtree(dest_base)  # remove existing directory for first run / another attempt

    rows=[]
    search = os.path.join(src, '**')
    for file in glob.glob(search, recursive=True):
        if ".json" not in file and not os.path.isdir(file):

            file_abs_initial = os.path.abspath(file)  # absolute file path
            file_rel_initial = os.path.relpath(file, src)  # file path relative to src
            file_name_initial = file_rel_initial.split('/')[-1]  # everything after last '/'

            file_size = os.path.getsize(file_abs_initial) / (1024 * 1024)  # convert bytes to megabytes
            file_size = round(file_size, 2)  # 2 == precision after decimal

            file_abs_final = os.path.join(dest_base, file_rel_initial)
            file_abs_final = os.path.abspath(file_abs_final)  # must be absolute for ghostcript

            # in case file is in sub-folder
            dest = os.path.dirname(file_abs_final)

            # ghost script will throw up if compression destination directories do not exist
            if not os.path.exists(dest):
                os.system(f'mkdir -p "{dest}"')  # don't know the equivalent in python

            # only compress files > 5 MB
            if file_size > 5:

                if file.endswith('.pdf'):  # could expand this someday to include images

                    if os.path.exists(file_abs_initial):
                        info = compress(file_abs_initial, file_abs_final, 2)
                        initial_size = info[0]
                        final_size = info[1]
                        compression_ratio = info[2]

                        # if we cannot do better than original, use it
                        if final_size > initial_size:
                            print(f"Compression Failed, Using Original File @ {initial_size}MB")
                            os.remove(file_abs_final)
                            shutil.copy(file_abs_initial, dest)

                        rows.append(
                            [file_rel_initial, initial_size, final_size, compression_ratio])

                else:
                    shutil.copy(file_abs_initial, dest)

            # if file > 64 Bytes, ie. not corrupted copy it over
            elif file_size * (1024 * 1024) > 64:

                # copy original file to Files_Reduced to further sort
                shutil.copy(file, dest)

    df = pd.DataFrame(rows, columns=['File', 'Initial Size (MB)', 'Final Size (MB)', 'Compression Ratio (%)'])
    print(df)

    # export dataframe to csv file
    df.to_csv('file_compress.csv', sep=',', encoding='utf-8')


def main():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('src', help='Path to file directory in need of compression')
    args = parser.parse_args()

    # Run
    file_reorg(args.src)


if __name__ == "__main__":
    # Executed when invoked directly, ie. `python file_compress.py`
    main()
