# interactions-files

[![PyPI - Downloads](https://img.shields.io/pypi/dm/interactions-files?color=blue&style=for-the-badge)](https://pypi.org/project/interactions-files/)
[![Version](https://img.shields.io/pypi/v/interactions-files?color=blue&style=for-the-badge)](https://pypi.org/project/interactions-files/)
[![Python Requirement](https://img.shields.io/pypi/pyversions/interactions-files?color=blue&style=for-the-badge)](https://pypi.org/project/interactions-files/)

An extension library for interactions.py allowing files in interaction responses.

# Table of Contents

- [Installation](#installation)
- [Information](#information)
- [Quickstart](#quickstart)
- [Documentation](#documentation)

# Installation

```bash
pip install -U interactions-files
```
# Information

This is `interactions-files`, an extension library for interactions.py allowing files in interaction responses.

By default, interactions.py does not allow you to send files in `CommandContext` and `ComponentContext`. This extension exists to solve that problem by adding `files` field to the `.send()` and `.edit()`.

# Quickstart

You can load `interactions-files` like every other Extension by using:
```py
client.load('interactions.ext.files')
```

After that, you can start sending files in Context. For example of doing this, go to [this](./examples).

Alternatively, you can use the functions provided by the Extension. Take a look at an example below:
```py
import io
import interactions
from interactions.ext.files import command_send

client = interactions.Client(token="Pfft!")

@client.command(
    name="file",
    description="Send a file.",
)
async def _test(ctx: interactions.CommandContext):
    txt = io.StringIO("This is a text file.")
    file = interactions.File(filename="file.txt", fp=txt)
    await command_send(ctx, "Below is a file.", files=file)

client.start()
```

For more information on the fuctions, check out the documentation.

# Documentation

[![API Reference](https://img.shields.io/badge/API-Reference-blue.svg?color=blue&style=for-the-badge)](https://github.com/interactions-py/files/wiki/API-Reference)
