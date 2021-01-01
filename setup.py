from distutils.core import setup
from setuptools import find_packages

REQUIREMENTS = [
    "requests==2.*",
    "pytz==2020.*",
]

REQUIREMENTS_DEV = [
    "mypy==0.*",
    "pytest==6.*",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mpyk",
    version="0.0.1",
    description="CLI tool and library for retrieving Wrocław public transit geolocation data",
    author="Mateusz Korzeniowski",
    author_email="emkor93@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emkor/mpyk",
    packages=find_packages(exclude=("test", "test.*")),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_DEV,
    extras_require={
        "dev": REQUIREMENTS_DEV
    },
    entry_points={
        "console_scripts": [
            "mpyk = mpyk.main:cli_main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Utilities"
    ],
)
