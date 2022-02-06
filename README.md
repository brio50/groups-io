# File Cleanup and Compression Utilities for [Hardinge Lathe Group](https://groups.io/g/hardinge-lathe)

There are 3 tiers of groups.io: basic (free), premium, and enterprise. We're on basic and have only 1GB of storage space for all files and photo albums. The tools herein allow for an admin to **Export Group Data** for processing by the python scripts herein. Instructions for export are available at https://groups.io/helpcenter/ownersmanual/1/exporting-or-downloading-your-group-s-data?single=true. One interesting quirk about the data export is that alongside `filename.ext` there is always `filename.ext.json` which includes metadata pertaining to that file.

---

`file_sweep.py` recursively searches a groups.io export directory specified and builds `file_sweep.csv` with rows that describe the File Name, URL, Extension, Size (MB), Created Date, Description, Category, Hardinge Lathe Model, Keep (Y/N), and an empty Note field for commentary. This file may then be imported into one's favorite online spreadsheet service, say sheets.google.com, to then collaborate on file deletion or reorganization based on file metrics.

`file_sweep.csv`:
```
,File,URL,Extension,Size (MB),Created,Description,Category,Model,Keep (Y/N),Note
0,AHC/AHCMain.pdf,https://groups.io/g/hardinge-lathe/files/AHC/AHCMain.pdf,.pdf,10.74,2016-03-16T03:53:26-07:00,AHC Maintenance Manual,manual,AHC;HC,Y,
1,AHC/AHCPL1.pdf,https://groups.io/g/hardinge-lathe/files/AHC/AHCPL1.pdf,.pdf,6.08,2016-03-16T03:44:37-07:00,AHC Parts List 72 pages,,AHC;HC,Y,
...
```


> **Note**: I wrote these scripts to work for any groups.io community. The only Haringe-Lathe group tailored component is guessing of "Category" and "Model" field names within `file_sweep.py`

> **Note**: If a shadow `*.json` file does not exist the tool is currently set to fail. The `Created` and `Description` fields would be missing.

---

`file_compress.py` is envisioned to help compress any file type extracted from a groups.io project, however as of this writing, it presently only compresses `*.pdf` files using [ghostscript](https://www.ghostscript.com). At this point, it's also worth mentioning that you'll need to install ghostscript for things to run properly. On a mac, open a terminal and type `brew install ghostscript`; on windows go to the [ghostscript website](https://www.ghostscript.com/), add the install location to your environment variables, and make sure to restart. The output is `file_compress.csv` which acts a file compression with metrics regarding Initial File Size (MB), Final File Size (MB), and Compression Ratio (%).

`file_compress.csv`:
```
,File,Initial Size (MB),Final Size (MB),Compression Ratio (%)
0,AHCMain2.pdf,7.21,2.6,63.9
1,AHCMain1.pdf,7.72,2.86,63.0
...
```

---

`main.py` calls both python scripts, and is where I selectively execute either `*sweep.py` or `*compress.py` from my Python IDE. This script shows the reader how to call the aforementioned `*.py` files.


---

* https://groups.io/helpcenter/membersmanual/1/working-with-databases/importing-a-json-or-csv-file

# File Organization:

```
# INDEX.CSV -- list of all files with descriptions
#
#   HISTORY (serial numbers, patents, etc.) := category == HISTORY
#   MANUAL LATHE CHANGE GEARING
#       TL, HLV, and HLV-H -- THIS IS COMMON TO ALL 3 LATHES up to 2008
#   MODEL-NUMBER/                           := model identified & ...
#       manuals/                            := category == MANUAL
#       brochures/
#       drawings/
#       threading/
#       misc*.ext                           := model identified & category empty
#   MODEL-UNKNOWN                           := model empty & category identified
#   MISC                                    := model empty & category empty
```

## MODEL NUMBERS:
* Cataract - 1939 AND EARLIER
* TL Series - Manual Tool Room Lathe - Most Activity lives here at this - 1939 to 1949
    * TL
    * T-10
    * T-5 
* HLV - Manual Tool Room Lathe - 1950 to 1959
* HLV-H - Manual Tool Room Lath - 1960 to 2008
* TR/ESM - Second Operation - 1930s to 1940s
* DV/DSM - Second Operation - 1940s to 2000s
* HC - Manual Chucker - ?
* AHC - Automatic Chucker - ?
* CNC - Newer - ?

> **NOTE**:`.jpg` were allowed in Files section at YAHOO. to GROUPS-IO transition, those were allowed to come through. Not certain if `.jpg` are still allowed in GROUPS-IO Files today. 
