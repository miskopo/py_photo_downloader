from setuptools import setup

setup(
    name='photo_downloader',
    version='0.0.2',
    packages=['photo_downloader'],
    entry_points={
        'console_scripts': [
            'photo_downloader = photo_downloader.__main__:main'
         ]
    })
