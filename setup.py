#!/usr/bin/env python3
"""
Setup script for Auto Sofalizer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="auto-sofalizer",
    version="2.0.0",
    author="Honey181",
    description="Automated SOFA-based spatial audio processing for video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Honey181/auto_sofalizer",
    py_modules=["auto_sofalizer"],
    python_requires=">=3.7",
    install_requires=[
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "auto-sofalizer=auto_sofalizer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    keywords="audio video sofa spatial-audio ffmpeg hrtf binaural",
    project_urls={
        "Bug Reports": "https://github.com/Honey181/auto_sofalizer/issues",
        "Source": "https://github.com/Honey181/auto_sofalizer",
        "Documentation": "https://github.com/Honey181/auto_sofalizer#readme",
    },
    include_package_data=True,
    package_data={
        "": ["*.sofa"],
    },
)

