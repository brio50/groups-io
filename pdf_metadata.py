from gs_compress import get_ghostscript_path
from datetime import datetime as dt
import subprocess
import sys
from file_sweep import json_read
import argparse


def pdf_metadata(file_abs):

    if ".pdf" not in file_abs:
        print(f"Error: input file is not a PDF: {file_abs}")
        sys.exit(1)

    json_dict = json_read(file_abs)
    json_name = json_dict['name']
    json_created = json_dict['created']
    json_desc = json_dict['desc']

    # https://rsmith.home.xs4all.nl/howto/pdf-tricks.html
    mod_date = dt.strftime(dt.now(), 'D:%Y%m%d%H%M%S')
    creation = dt.strptime(json_created, '%Y-%m-%dT%H:%M:%S%z') #2016-03-16T03:53:26-07:00
    crt_date = dt.strftime(creation, 'D:%Y%m%d%H%M%S')

    # https://unix.stackexchange.com/questions/489230/where-is-metadata-for-pdf-files-can-i-insert-metadata-into-any-pdf-file
    metadata = (f"[ /Title ({json_name})\n"
                f"  /Author (https://groups.io/g/hardinge-lathe/)\n"
                f"  /Subject ({json_desc})\n"
                f"  /Creator (Hardinge Lathe Group)\n"
                f"  /ModDate ({mod_date})\n"
                f"  /Producer ()\n"
                f"  /Keywords ()\n"
                f"  /CreationDate ({crt_date})\n"
                f"  /DOCINFO\n"
                f"pdfmark\n")

    # save metadata into text file: <filename>.pdfmark
    file_pdfmark = file_abs.replace(".pdf", ".pdfmark")
    with open(file_pdfmark, "w+") as f:
        f.writelines(metadata)

    gs = get_ghostscript_path()
    cmd = [gs,
           '-sDEVICE=pdfwrite',
           '-o {}'.format(file_abs),
           file_abs,
           f'{file_pdfmark}'
           ]

    try:
        # execute
        subprocess.call(cmd, stderr=sys.stdout)
    except:
        # print ghostscript command for debug
        print(" ".join(cmd))


def main(file_rel, json_created, json_desc, category, model):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file_abs', help='Path to PDF file in need of metadata')
    args = parser.parse_args()

    # Run
    pdf_metadata(args.file_abs)

if __name__ == "__main__":
    # Executed when invoked directly, ie. `python file_compress.py`
    main()