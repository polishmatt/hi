from setuptools import setup
import importlib

setup(
    name='hicli',
    description='A generic CLI for connecting humans to host interfaces.',
    long_description="""
A configurable shorthand for interfacing with external hosts.
Arguments are individually matched against a set of specified hosts. If one result is found the command to interface with that host is run. Otherwise, all matching hosts are printed.
    """,
    author='Matt Wisniewski',
    author_email='hicli@mattw.life',
    license='GPLv3',
    url='https://github.com/polishmatt/hi',
    keywords=['hi', 'cli', 'hicli', 'utility', 'host', 'interface'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    platforms=['unix','linux'],
    packages=[
        'hicli'
    ],
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'hi = hicli.cli:cli'
        ],
    },
)
