from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interactions-files",
    version="1.0.0",
    description="Add files into CommandContext sending",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jimmy-Blue/interactions-files",
    author="Jimmy-Blue",
    author_email="jummyblue00@duck.com",
    license="MIT",
    packages=["interactions.ext.files"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "discord-py-interactions>=4.2.0",
    ],
)