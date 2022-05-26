# interactions-files
An external for interactions.py to add ``files`` into CommandContext send.

# How to use

It is pretty straight forward. Here is an example.
```py
import interactions

client = interactions.Client(...)

client.load('interactions.ext.files')
```

After that, you can use use ``files`` in CommandContext to send file. Take an example below.
```py
import interactions
import io

client = interactions.Client(...)
client.load('interactions.ext.files')


async def test(ctx: interactions.CommandContext):
    data = "Hey look, this is a file from CommandContext."
    file = io.StringIO(data)
    with file as f:
        file = interactions.File(filename="aaaaa.txt", fp=f)
        await ctx.send(files=file)


client.start()
```

You can use it in an ``Extension``, a.k.a Cogs. Just load ``interactions.ext.files`` and you are done.

# Credits

- Credits to [Toricane](https://github.com/Toricane) for the original idea.
