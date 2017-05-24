
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='mp3PCDLer',

    version='0.0.1',

    description=" Simple Front-End wrapper for downloading youtube videos/movies based off of rg3's yt-dl Command Line Application ",
    long_description='',#long_description,

    # The project's main homepage.
    url='https://github.com/BC7/mp3PCDLer',

    # Author details
    author='BC7',
    author_email='brian.ngobidi@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Desktop Environment :: File Managers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='youtube mp3 downloading ID3 tag editting',
    packages=['mp3PCDLer'],
    install_requires=['youtube-dl',"eyed3"],

    entry_points={
    'console_scripts': [
        'mp3PCDLer = mp3PCDLer.__main__:main',
    	],
	},

    package_data={
        'mp3PCDLer': ['pref.json'],
    },

)
