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

@client.command(
    name="file",
    description="Send a message as a text file",
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="message",
            description="Message",
            required=True
        )
    ]
)
async def _file(ctx: interactions.CommandContext, message: str):
    file = io.StringIO(message)
    with file as f:
        file = interactions.File(filename="message.txt", fp=f)
        await ctx.send(files=file)


client.start()
```

You can use it in an ``Extension``, a.k.a Cogs. Just load ``interactions.ext.files`` and you are done.

# Credits

- Credits to [Toricane](https://github.com/Toricane) for the original idea.
