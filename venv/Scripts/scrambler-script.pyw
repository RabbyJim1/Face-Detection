#!C:\Users\rabby\PycharmProjects\untitled\venv\Scripts\pythonw.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'face-scrambler==0.0.2','gui_scripts','scrambler'
__requires__ = 'face-scrambler==0.0.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('face-scrambler==0.0.2', 'gui_scripts', 'scrambler')()
    )
