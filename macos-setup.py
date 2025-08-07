from setuptools import setup

APP = ['SlashCode.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,
    'includes': [],
    'plist': {
        'CFBundleIdentifier': 'com.clydezzz-sleepy.slashcode',
    },
    'bdist_base': 'build',
    'packages': [],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
