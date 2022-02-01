from file_sweep import *
from file_reorg import *
import os

src = os.path.join('hardinge-lathe', 'Files')
url_base = 'https://groups.io/g/hardinge-lathe/files/'

# uncomment/comment as desired
file_sweep(src, url_base)
file_reorg(src)

# after re-organization complete, add metadata to pdfs
#pdf_metadata()
