"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['app.py']
DATA_FILES = []

OPTIONS = {'argv_emulation': True,
           'plist': {
               'PyRuntimeLocations': [
                '@executable_path/../Frameworks/libpython3.6m.dylib',
                '/Applications/anaconda3/lib/libpython3.6m.dylib'
               ]
           }}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
