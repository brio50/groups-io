import os
from gs_compress import *
import pandas as pd
import argparse


def isNaN(num):
    return num != num

def file_reorg(src):

    # concatenate "<src> + _Reduced" to form compression destination directory
    dest_base = src.rstrip(os.sep) + '_Reorg'
    if os.path.exists(dest_base):
        shutil.rmtree(dest_base)  # remove existing directory for first run / another attempt

    # use file_sweep.csv to serve as basis for file reoganization
    csv = pd.read_csv('file_sweep.csv')

    rows=[]
    for ind in csv.index:

        file = csv['File'][ind]
        category = csv['Category'][ind]
        model = csv['Model'][ind]

        file_abs_initial = os.path.join(src, file)
        file_abs_initial = os.path.abspath(file_abs_initial)  # absolute file path
        file_rel_initial = os.path.relpath(file_abs_initial, src)  # file path relative to src
        file_name = file_rel_initial.split(os.sep)[-1]
        file_size = os.path.getsize(file_abs_initial) / (1024 * 1024)  # convert bytes to megabytes
        file_size = round(file_size, 2)  # 2 == precision after decimal

        # only process files that aren't corrupt, ie. > 64 KB
        if file_size * (1024 * 1024) > 64:





            # File Organization:
            #   HISTORY (serial numbers, patents, etc.) := category == HISTORY
            #   MANUAL LATHE CHANGE GEARING
            #       TL, HLV, and HLV-H
            #   MODEL-NUMBER/                           := model identified & ...
            #       manuals/                            := category == MANUAL
            #       brochures/
            #       drawings/
            #       threading/
            #       misc*.ext                           := model identified & category empty
            #   MODEL-UNKNOWN                           := model empty & category identified
            #   MISC                                    := model empty & category empty


            if isNaN(model) and isNaN(category):
                subfolder = os.path.join(dest_base, 'MISC')
            elif isNaN(model) and not isNaN(category):
                subfolder = os.path.join(dest_base, 'MODEL-UNKNOWN', category)
            elif not isNaN(model) and isNaN(category):
                subfolder = os.path.join(dest_base, model)
            elif not isNaN(model) and not isNaN(category):
                subfolder = os.path.join(dest_base, model, category)
            elif not isNaN(category) and 'history' in category:
                subfolder = os.path.join(dest_base, 'HISTORY')

            dest = os.path.abspath(subfolder)  # must be absolute for ghostcript
            file_abs_final = os.path.join(dest, file_name)

            # ghost script will throw up if compression destination directories do not exist
            if not os.path.exists(dest):
                os.makedirs(dest)

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

            else:

                # copy original file to Files_Reorg to further sort
                shutil.copy(file_abs_initial, dest)

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
