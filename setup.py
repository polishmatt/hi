from setuptools import setup
import importlib

version = importlib.import_module('hi.config').version

setup(
    name='hi',
    version=version,
    description='',
    long_description="",
    author='Matt Wisniewski',
    author_email='hicli@mattw.us',
    license='MIT',
    url='https://github.com/polishmatt/hi',
    keywords=[''],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
