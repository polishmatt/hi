from setuptools import setup
import importlib

version = importlib.import_module('hi.config').version

setup(
    name='hicli',
    version=version,
    description='A generic CLI for connecting humans to host interfaces.',
    long_description="""
A configurable shorthand for interfacing with external hosts.
Arguments are individually matched against a set of specified hosts. If one result is found the command to interface with that host is run. Otherwise, all matching hosts are printed.
    """,
    author='Matt Wisniewski',
    author_email='hicli@mattw.us',
    url='https://github.com/polishmatt/hi',
    keywords=['hi', 'cli', 'utility', 'host', 'interface'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    platforms=['unix','linux'],
    packages=[
        'hi'
    ],
    install_requires=[
        'click==6.7',
        'pyyaml==3.12'
    ],
    entry_points={
        'console_scripts': [
            'hi = hi.cli:cli'
        ],
    },
)
