from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interactions-files",
    version="1.1.5",
    description="An extension library for interactions.py allowing files in interaction responses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/interactions-py/files",
    author="Jimmy-Blue",
    author_email="jimmyblue00@duck.com",
    license="MIT",
    packages=["interactions.ext.files"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "discord-py-interactions>=4.3.0",
    ],
)
