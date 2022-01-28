# File Cleanup Utilities for [Hardinge Lathe Group](https://groups.io/g/hardinge-lathe)

There are 3 tiers of groups.io: basic (free), premium, and enterprise. We're on basic and have only 1GB of storage space for all files and photo albums. The tools herein allow for an admin to **Export Group Data** for processing by the python scripts herein. Instructions for export are available at https://groups.io/helpcenter/ownersmanual/1/exporting-or-downloading-your-group-s-data?single=true. One interesting quirk about the data export is that alongside `filename.ext` there is always `filename.ext.json` which includes metadata pertaining to that file.

`file_sweep.py` recursively searches a groups.io export directory specified and builds `file_compress.csv` with rows that describe the File Name, URL, Extension, Size (MB), Created Date, Description, Category, Hardinge Lathe Model, Keep (Y/N), and an empty Note field for commentary. This file may then be imported into one's favorite online spreadsheet service, say sheets.google.com, to then collaborate on file deletion or reorganization based on file metrics.

`file_compress.py` is envisioned to help compress any file type extracted from a groups.io project, however as of this writing, it presently only compresses `*.pdf` files using [ghostscript](https://www.ghostscript.com). At this point, it's also worth noting that this code was developed on a mac; to install ghostscript, open a terminal and type `brew install ghostscript`. The output is `file_sweep.csv` which acts a file compression with metrics regarding Initial File Size (MB), Final File Size (MB), and Compression Ratio (%).

`main.py` calls both python scripts, and is where I selectively execute either `*sweep.py` or `*compress.py` from my Python IDE. This script shows the reader how to call the aforementioned `*.py` files.

