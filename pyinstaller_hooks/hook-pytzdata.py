# pyinstaller_hooks/hook-pytzdata.py

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("pytzdata", include_py_files=True)